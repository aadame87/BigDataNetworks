import networkx as nx
import community
import igraph
import cairocffi


#G=nx.read_gml("erdoscom.gml")
#print(nx.info(G))

iG=igraph.Graph()
iG=igraph.read("erdos.gml")
print (igraph.summary(iG))
print(iG)
#vertDendo=iG.community_fastgreedy()
#print(vertDendo.membership)
igraph.plot(iG)
