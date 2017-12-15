#%%time
#import useful packages, all of them are important but not necessarily used in this code
#enable inline plotting in Python Notebook
#supress warnings

#%pylab inline
import networkx as nx
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import scipy
import warnings
warnings.filterwarnings('ignore')
import time
#%%time
# Creating directories for network files:
import os, errno
try:
    os.makedirs("data")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.makedirs("data/facebook")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

try:
    os.makedirs("data/enron")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.makedirs("data/citNet")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

try:
    os.makedirs("data/erdos")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


# Download the network files:
import urllib

## Facebook Network:
urllib.urlretrieve("https://snap.stanford.edu/data/facebook_combined.txt.gz","data/facebook/facebook_combined.txt.gz")

## Citation Network:
urllib.urlretrieve("http://snap.stanford.edu/data/cit-HepTh.txt.gz", "data/citNet/cit-HepTh.txt.gz")
urllib.urlretrieve("http://snap.stanford.edu/data/cit-HepTh-dates.txt.gz", "data/citNet/cit-HepTh-dates.txt.gz")
urllib.urlretrieve("http://snap.stanford.edu/data/cit-HepTh-abstracts.tar.gz", "data/citNet/cit-HepTh-abstracts.tar.gz")


## Enron Network:
urllib.urlretrieve("https://snap.stanford.edu/data/email-Enron.txt.gz","data/enron/email-Enron.txt.gz")

## Erdos Network:
urllib.urlretrieve("https://files.oakland.edu/users/grossman/enp/Erdos1.html", "data/erdos/Erdos1.html")

# The following code simply converts the data file from ZIP to TXT so that NetworkX can read it

import gzip
inF = gzip.GzipFile("data/facebook/facebook_combined.txt.gz", 'rb')
s = inF.read()
inF.close()

outF = file("data/facebook/facebook_combined.txt", 'wb')
outF.write(s)
outF.close()

#load the network after converting into text file

file_name="data/facebook/facebook_combined.txt"

#convert the information in the text file into a graph, find no. of edges & nodes in the graph

g1=nx.read_edgelist(file_name,create_using=nx.Graph(),nodetype=int)
node, edge=g1.order(),g1.size()
print "No. of nodes are=",node
print "No. of edges are=",edge

degs={}
for n in g1.nodes():
    deg=g1.degree(n)
    if deg not in degs:
        degs[deg]=0
    degs[deg]+=1
items=sorted(degs.items())

fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot([k for (k,v) in items], [v for (k,v) in items])
ax.set_xscale('log')
ax.set_yscale('log')
plt.title("homework1 deg dist")
fig.savefig("deg_dist1.png")
print "figure saved"

'''
print "is connected:",nx.is_connected(g1)
#nx.number_connected_components(g1)

print "diameter: ",nx.diameter(g1)
print "avg shortest path: ",nx.average_shortest_path_length(g1)

d= nx.clustering(g1)
hist(d.values(),bins=50)
show()

c= nx.degree_centrality(g1)
hist(c.values(),bins=75)
show()

cn= nx.closeness_centrality(g1)
hist(cn.values(),bins=75)
show()
'''

from multiprocessing import Pool
import itertools

def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x

def _betmap(G_normalized_weight_sources_tuple):
    """Pool for multiprocess only accepts functions with one argument.
    This function uses a tuple as its only argument. We use a named tuple for
    python 3 compatibility, and then unpack it when we send it to
    `betweenness_centrality_source`
    """
    return nx.betweenness_centrality_subset(*G_normalized_weight_sources_tuple)

def betweenness_centrality_parallel(G, processes=4):
    """Parallel betweenness centrality function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool)*4
    node_chunks = list(chunks(G.nodes(), int(G.order()/node_divisor)))
    # print node_chunks
    num_chunks = len(node_chunks)

    bt_sc = p.map(_betmap,
                 zip([G]*num_chunks,
                    node_chunks,
                    [list(G)]*num_chunks,
                    [True]*num_chunks,
                    [None]*num_chunks))

    # print bt_sc
    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

bn_cent=betweenness_centrality_parallel(g1)


nx.set_node_attributes(g1, bn_cent,"betweeness")
nx.set_node_attributes(g1, degs,"deg dist")
