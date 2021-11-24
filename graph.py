from networkx.readwrite.json_graph import adjacency
from numpy import genfromtxt
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import io
import pydot
df = pd.read_csv('ModernMCU.csv')
print(df)
# G=nx.DiGraph(mydata.values)
# nx.draw(G)
#myData = genfromtxt('mcuComics.csv', delimiter=',')
#print(myData)
# adjacency = myData[1:,1:]
#print(adjacency)

G = nx.DiGraph()
for col in df: 
    for x in list(df.loc[df[col] == 1, 'hero']):
        G.add_edge(col, x)

G.edges()
nx.draw(G, nx.shell_layout(G))
plt.show()
#show_graph_with_labels(adjacency, make_label_dict(get_labels('mycsv.csv')))
# def draw_graph(graph):

#     # extract nodes from graph
#     nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

#     # create networkx graph
#     G=nx.Graph()

#     # add nodes
#     for node in nodes:
#         G.add_node(node)

#     # add edges
#     for edge in graph:
#         G.add_edge(edge[0], edge[1])

#     # draw graph
#     pos = nx.shell_layout(G)
#     nx.draw(G, pos)

#     # show graph
#     plt.show()

# # draw example
# graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
# #draw_graph(graph)