import networkx as nx
g = nx.read_gml("graph.gml")

print g[1186][1412]['weight']
