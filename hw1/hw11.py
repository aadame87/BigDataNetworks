
# coding: utf-8

# # Homework #1
# ## In this homework you are going to get familiar with basics of NetworkX and Gephi for analysing and visualizing networks. Make sure your submitted code is executable without any errors. Also, make sure to include all your output files in your submission.
#
# ## Task 1: NetworkX
# ### NetworkX is a Python library for the analysis of networks. With NetworkX you can create, import, and manipulate graphs. Additionally, you can calculate basic properties of these graphs with its built-in functions. Unfortunately, NetworkX is not very powerful for visualizing large graphs which we are going to work with most of the time. For this reason, we are going to use a software called Gephi. In this homework, you are going to do some basic analysis on some graphs which you can download using the following code and then store the results in a format which is readable by Gephi. You then use Gephi (on your own computer) to visualize the results.
#
# ### You can download Gephi from the following web page:
# ### https://gephi.org/users/download
#
# ###  You can also learn the basics of NetworkX library and Gephi by looking at the following pages:
# ### Some useful links to get familiar with NetworkX:
# ### NetworkX Documentation: https://networkx.github.io/documentation/stable/
# ### https://vimeo.com/124354692
# ### https://www.cl.cam.ac.uk/~cm542/teaching/2010/stna-pdfs/stna-lecture8.pdf
# ### Some useful links to get familiar with Gephi:
# ### https://gephi.org/users/tutorial-visualization/
# ### https://www.youtube.com/watch?v=FLiv3xnEepw
#
# ### In the whole homework you can use any function from the NetworkX  library that facilitates your task.

# ### Run the following cell to import the libraries that we are going to use in this homework:

# In[1]:

#import useful packages, all of them are important but not necessarily used in this code
#enable inline plotting in Python Notebook
#supress warnings

import networkx as nx
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import scipy
import warnings
warnings.filterwarnings('ignore')
import time


# ### Run the following cell to download the raw data for the networks (Facebook, Enron Emails, High Energy Physics Citations, and Erdos) we are going to work with:

# In[2]:

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

# ### Run the following cell to unzip and store the Facebook dateset in a .txt file which is readable by NetworkX:

# In[3]:
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

#citation network
inF = gzip.GzipFile("data/citNet/cit-HepTh.txt.gz", 'rb')
s = inF.read()
inF.close()

outF = file("data/citNet/cit-HepTh.txt", 'wb')
outF.write(s)
outF.close()

#load the network after converting into text file

file_name="data/citNet/cit-HepTh.txt"

#convert the information in the text file into a graph, find no. of edges & nodes in the graph

g2=nx.read_edgelist(file_name,create_using=nx.Graph(),nodetype=int)
node, edge=g2.order(),g2.size()
print "No. of nodes are=",node
print "No. of edges are=",edge
# ### Write a code that plots the degree distribution of the above graph. (Make sure you do not confuse degree distribution with degree sequence!)

# In[4]:


'''
Your code here.
adapted from http://snap.stanford.edu/class/cs224w-2012/nx_tutorial.pdf
'''

degs={}
for n in g1.nodes():
    deg=g1.degree(n)
    if deg not in degs:
        degs[deg]=0
    degs[deg]+=1
items=sorted(degs.items())
'''
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot([k for (k,v) in items], [v for (k,v) in items])
ax.set_xscale('log')
ax.set_yscale('log')
plt.title("FB Degree Dist")
fig.savefig("deg_dist1.png")
print "figure saved"
'''
#citnet code
degs2={}
for n in g2.nodes():
    deg=g2.degree(n)
    if deg not in degs2:
        degs2[deg]=0
    degs2[deg]+=1
items=sorted(degs2.items())
'''
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot([k for (k,v) in items], [v for (k,v) in items])
ax.set_xscale('log')
ax.set_yscale('log')
plt.title("CitNet Degree Dist")
fig.savefig("deg_dist2.png")
print "figure saved2"
'''

# ### Determine whether the above graph is connected or not. Otherwise, find and store its largest connected component.

# In[5]:

print "is FB connected:",nx.is_connected(g1)
#nx.number_connected_components(g1)

#citnet code
print "is CitNet connected:",nx.is_connected(g2)
print "number of connected components:", nx.number_connected_components(g2)
#print "is graph directed:", nx.is_directed(g2)

#get largest component
Gcc = sorted(nx.connected_component_subgraphs(g2), key=len, reverse=True)
g22 = Gcc[0]
print "is CitNet subgraph connected:", nx.is_connected(g22)


# ###  Write a code that calculates and prints the network diameter and the average shortest path between any two nodes in the network.

# In[ ]:


'''
Your code here
'''
#print "calculating ecc"
#ecc=nx.eccentricity(g1)
#print "calculating diameter"
#print "FB diameter: ",nx.diameter(g1,ecc)
#print "FB avg shortest path: ",nx.average_shortest_path_length(g1)


#citnet code
print "calculating ecc"
ecc=nx.eccentricity(g22)
print "calculating diameter"
print "CitNet diameter: ",nx.diameter(g22,ecc)
#print "CitNet avg shortest path: ",nx.average_shortest_path_length(g22)


# ### Write a code to calculate the clustering coeffient of the nodes of the graph and plot it as a histogram.

# In[43]:


'''
Your code here
'''
#d1 = nx.clustering(g1)
#hist(d1.values(),bins=50)
#show()

#d2 = nx.clustering(g22)
#hist(d2.values(),bins=50)
#show()


# ### Write a code to calculate the degree centrality of the nodes of the graph and plot it as a histogram.

# In[48]:


'''
Your code here
'''
#c1= nx.degree_centrality(g1)
#hist(c1.values(),bins=75)
#show()

#c2= nx.degree_centrality(g22)
#print "deg centrality calculated"
#hist(c2.values(),bins=100)
#show()





# ### Write a code to calculate the betweenness centrality of the nodes of the graph and plot it and plot it as a histogram.

# In[26]:


'''
Your code here
This is calculated in the cell below
'''
#bb = nx.betweenness_centrality(g1)
#cn= nx.closeness_centrality(g1)
#hist(cn.values(),bins=75)
#show()



# ### Write a code to calculate the eigenvector centrality of the nodes of the graph and plot it in as a histogram.

# In[49]:


'''
Your code here
'''
#centrality = nx.eigenvector_centrality(g1)
#print "eigenval 1 calculated"
#hist(centrality.values(),bins=60)
#show()

#centrality2 = nx.eigenvector_centrality(g22)
#print "eigenval 2 calculated"
#hist(centrality2.values(),bins=60)
#show()


# ### Write a code to store the graph in a file that is readable by Gephi (Hint: Use NetworkX write_gml method.) Make sure to add the betweenness centrality and degree of each node as an attribute of each node to be stored in this file for the next tasks.

# In[25]:


'''
Your code here
'''
#print degs
#print bn_cent
#nx.set_node_attributes(g1, bn_cent,"betweenness")
#nx.set_node_attributes(g1, degs,"degdist")
#nx.write_gml(g1,"test.gml")


# ### <font color='red'> Repeat this task for all the other three networks. </font>
# ### (Use the following code to create the Erdos graph in NetworkX.)

# In[13]:


# In[14]:



# ### For larger networks, in case the calculation of the betweenness centrality takes a long time, you can use the  following faster code which uses all the cores of the processing unit.

# In[6]:


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
#changed 4 to 2
def betweenness_centrality_parallel(G, processes=2):
    """Parallel betweenness centrality function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool)*2 #chnaged 4 to 2
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


# In[ ]:


'''
Your code here.
'''
#bn_cent=betweenness_centrality_parallel(g1)
#hist(bn_cent.values())
#show()
'''
print "starting bn_cent2..."
bn_cent2=betweenness_centrality_parallel(g22)
print "bn_cent2 completed"

print "starting to write file"
fout = "bn_cent2.txt"
fo = open(fout, "w")

for k, v in bn_cent2.items():
    fo.write(str(k) + ' >>> '+ str(v) + '\n\n')
fo.close()
print "finished writing file"
#hist(bn_cent2.values())
#show()
'''

'''
if __name__ == "__main__":
    G_ba = nx.barabasi_albert_graph(1000, 3)
    G_er = nx.gnp_random_graph(1000, 0.01)
    G_ws = nx.connected_watts_strogatz_graph(1000, 4, 0.1)
    for G in [G_ba, G_er, G_ws]:
        print("")
        print("Computing betweenness centrality for:")
        print(nx.info(G))
        print("\tParallel version")
        start = time.time()
        bt = betweenness_centrality_parallel(G)
        print("\t\tTime: %.4F" % (time.time() - start))
        print("\t\tBetweenness centrality for node 0: %.5f" % (bt[0]))
        print("\tNon-Parallel version")
        start = time.time()
        bt = nx.betweenness_centrality(G)
        print("\t\tTime: %.4F seconds" % (time.time() - start))
        print("\t\tBetweenness centrality for node 0: %.5f" % (bt[0]))
    print("")

    nx.draw(G_ba,node_size=10,width=0.05)
    plt.show()
    '''


# ## Task 2: Gephi
# ### In this task we will use Gephi to visualize the networks that you analyzed. In the previous task, you saved the graph in the gml format such that each node has the degree and its betweenness centrality as its attribute. In this task you are going to use these attributes to have a better visualization of the graph. Follow these steps to find a nice and meaningfull visualization of the graphs:
#
# ### Open Gephi-->> Open the '.gml' file of a network -->> Change 'Layout' of the graph (e.g., to Force Atlas 2, etc.) to have a better visualisation -->> In 'Appearance' window there are multiple options to change appearance of the nodes/ edges of the graph according to the various network properties like degree, clustering coefficient, modularity class, etc.-->> Change node size according to Degree distribution. -->> Save image file and include it in the following cell for each of the above networks.
#
# ### Repeat the above procedure using betweenness centrality.
#
# ### In addition to including all your visulizations for each of the four networks in your notebook, include the GML and SVG formats of these visulizaitons in your submission.
#
# ### Answer these questions for the citation and Erdos networks:
# ### -- Label the nodes with the name of the authors such that the font size is proportional to the size of the node.
# ### -- Based on your visualizations who is the author with the largest node? Is this conclusion consistent across the two visulizations (using degree and betweenness centrality) of the graph? What about the author with the second largest node?
#

# In[ ]:


'''
Your code here.
'''


# In[ ]:


'''
Your visulizations here.
'''
