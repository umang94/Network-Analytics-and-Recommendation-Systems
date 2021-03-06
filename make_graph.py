#!/usr/bin/env python
""" Code for reading raw table data from the csv file and making the complete graph file and dumping it into a gml file for further use of commuity extraxtion"""
import csv
import igraph
import json

g = igraph.Graph()

description_map = {}

with open('raw_data/repo-attributes.csv', 'rb') as repofile:
    reader = csv.DictReader(repofile)
    for repo in reader:
        g.add_vertex(name=repo['repository_url'],
            label=repo['repository_url'][19:],
            language='(unknown)' if repo['repository_language'] == 'null'
                else repo['repository_language'],
            watchers=int(repo['repository_watchers']))
        description = repo['repository_description']
        label = repo['repository_url'][19:]
        description_map[label] = description


with open('raw_data/repo-weights.csv', 'rb') as edgefile:
    reader = csv.DictReader(edgefile)
    for edge in reader:
        g.add_edge(edge['repository1'], edge['repository2'],
            weight=float(edge['weight']))

print g.summary()

writer = csv.writer(open('descriptions/description_map.csv', 'wb'))
for key, value in description_map.items():
   writer.writerow([key, value])

#communities = g.community_fastgreedy()
#optimal_number =  communities.optimal_count

#clusters = communities.as_clustering(optimal_number)
#print len(clusters)

ed =  g.incident(1186)
for e in ed:
  print e, g.es[e]['weight']

adj_l = g.get_adjedgelist()
print adj_l[1186]
adj_v = g.neighborhood(94)
print adj_v


n = g.vs[1186]

print n['name']

try:
  g.vs.find(name = "hello")
except ValueError:
  print "Works"

#print g.get_edgelist()
matrix =  g.get_adjacency()

#print len(matrix[0])

ed = g.es.select(_source = 1725, _target = 1715)
print ed['weight']
print matrix[1725][1715]


#membership= clusters.membership

#print len(membership)
#print clusters[0], clusters[1]
#print max(communities.as_clustering().membership)
g.write('graph.gml')
