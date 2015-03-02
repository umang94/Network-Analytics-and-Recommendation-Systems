#!/usr/bin/env python
import csv
import igraph

g = igraph.Graph()

with open('data/repo-attributes.csv', 'rb') as repofile:
    reader = csv.DictReader(repofile)
    for repo in reader:
        g.add_vertex(name=repo['repository_url'],
            label=repo['repository_url'][19:],
            language='(unknown)' if repo['repository_language'] == 'null'
                else repo['repository_language'],
            watchers=int(repo['repository_watchers']))

with open('data/repo-weights.csv', 'rb') as edgefile:
    reader = csv.DictReader(edgefile)
    for edge in reader:
        g.add_edge(edge['repository1'], edge['repository2'],
            weight=float(edge['weight']))

print g.summary()
#igraph.plot(g)
g.write('graph.gml')
