import igraph,csv;

newGraph = igraph.Graph()

def add_node():
  global  newGraph
  with open('data/results-20141004-141029.csv') as repository_data:
    data = csv.DictReader(repository_data)
    for repository in data:
      newGraph.add_vertex(name=repository['repository_url'],label=repository['repository_url'][19:],language=repository['repository_language'],watchers=int(repository['repository_watchers']))
        
add_node()
print newGraph.summary()
newGraph.write("output.gml")
