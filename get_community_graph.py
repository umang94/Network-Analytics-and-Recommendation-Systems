import igraph
import sys
import getopt

def load_graph_from_csv(filename):
  g = igraph.Graph()
  with open('repo-attributes.csv', 'rb') as repofile:
    reader = csv.DictReader(repofile)
    for repo in reader:
        g.add_vertex(name=repo['repository_url'],
            label=repo['repository_url'][19:],
            language='(unknown)' if repo['repository_language'] == 'null'
                else repo['repository_language'],
            watchers=int(repo['repository_watchers']))

  with open('repo-weights.csv', 'rb') as edgefile:
    reader = csv.DictReader(edgefile)
    for edge in reader:
      g.add_edge(edge['repository1'], edge['repository2'],
            weight=float(edge['weight']))
      
  return g

def language_stats(graph):
  language_count = {}
  for node in graph.vs:
    language = node['language']
    if not language_count.has_key(language): 
      language_count[language] = 1
    else : 
      language_count[language] += 1
  return language_count

def display_statistics(filename):
  graph = load_graph(filename)
  statistics = language_stats(graph)
  print "Language".rjust(20) , "Sub Graph Size".rjust(20)
  for key, value in statistics.iteritems():
    print key.rjust(20) , str(value).rjust(20) 

def getting_communities(graph):
  communities = graph.community_fastgreedy()
  optimal_number = communities.optimal_count
  clusters = communities.as_clustering(optimal_number)
  count  = 0
  for cluster in clusters:
    count += 1
    for id in cluster :
      print "Cluster ID : ", count , " Node : ",  graph.vs[id]['name'], " Language : " , graph.vs[id]['language']

def load_graph(filename):
  g = igraph.read(filename)
  return g

def get_language_nodes(graph, language):
  language_nodes = []
  for node in graph.vs:
    if node['language'] == language:
      language_nodes.append(node['id'])
  return language_nodes

complete_graph = load_graph("graph.gml")

def generate_community_graph(complete_graph, language_nodes):
  community_graph = igraph.Graph()

  for node_i in language_nodes:
    node = complete_graph.vs[int(node_i)] 
    try:
      community_graph.vs.find(name=node['name'])
    except KeyError:
      print "Adding Node : ", node['name'] , " Language : " , node['language']
      community_graph.add_vertex(name = node['name'],
          label = node['label'],
          language = node['language'],
          watchers = node['watchers'])
    except ValueError:
      print "Adding Node : ", node['name'] , " Langauge : " , node['language']
      community_graph.add_vertex(name = node['name'],
          label = node['label'],
          language = node['language'],
          watchers = node['watchers'])
    neighbour_nodes = complete_graph.neighborhood(int(node['id']))
    
    for node_id in neighbour_nodes:
      current_node = complete_graph.vs[int (node_id )]
      
#Adding neighbour node to the graph

      try:
        community_graph.vs.find(name=current_node['name'])
      except KeyError:
        print "Adding Node : ", current_node['name'] , " Language : " , current_node['language']
        community_graph.add_vertex(name = current_node['name'],
          label = node['label'],
          language = node['language'],
          watchers = node['watchers'])
      except ValueError:
        community_graph.add_vertex(name = current_node['name'],
            label = current_node['label'],
            language = node['language'],
            watchers = node['watchers'])

      #Adding an edge
      if node['id']  != current_node['id']:
        original_edge = complete_graph.es.select(_source = int(node['id']), _target = node_id)
        ed_weight = original_edge['weight']
        if len(ed_weight) == 0:
          ed_weight = 1
        else:
          ed_weight = ed_weight[0]
        print "Adding Edge - Weight : " , ed_weight , " Source : ", node['name'] , " Target : ", current_node['name']
        community_graph.add_edge(node['name'],current_node['name'],weight=ed_weight)

  return community_graph

  
def initializer(language, filename):
  complete_graph = load_graph(filename)
  language_nodes = get_language_nodes(complete_graph, language)
  community_graph = generate_community_graph(complete_graph,language_nodes)
  output = language + ".gml"
  #getting_communities(complete_graph)
  print language_stats(complete_graph)
  community_graph.write(output)
  #layout = complete_graph.layout_fruchterman_reingold()
  #igraph.plot(community_graph,layout=layout, vertex_label = None, vertex_size = 5)
  
#print complete_graph.summary()

#language_nodes = get_language_nodes(complete_graph,"JavaScript")


#for node_id in language_nodes:
#  node = complete_graph.vs[int(node_id)]
#  print node['id'], node['name'], node_id
#community_graph = generate_community_graph(complete_graph,language_nodes)

#print community_graph.summary()

#community_graph.write('python.gml')


def main():
  has_file = False
  display_stats = False
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hf:l:s:",["help","filename","language","statistics"])
  except getopt.GetoptError as err:
      print str(err)
      print "Usage : python get_community_graph.py -f <complete_graph_filename> -l <language> -s <Optional Langauge Statistics>"
      sys.exit()
  if len(opts) == 2 or len(opts) == 3 : 
      for opt , arg  in opts:
          if opt == "-h":
              print "Usage : python get_community_graph.py -f <complete_graph_filename> -l <language> -s <Optional Language Statistics>"
              sys.exit()
          elif opt in ("-f", "--filename"):
            has_file = True
            filename = arg
            if display_stats:
              display_statistics(filename)
              sys.exit()
          elif opt in ("-l", "--language"):
            language = arg
          elif opt in ("-s", "--statistics"):
            display_stats = True
            if has_file:
              display_statistics(filename)
              sys.exit()

#  elif len(opts) == 3:
 #   for opt , arg in opts:
  #    if opt in ("-s", "--statistics"):
   #     display_stats = True
    #    if has_file :
     #     display_statistics(filename)
      #    sys.exit()
      #if opt in ("-f", "--filename"):
       # has_file = True
        #if display_stats:
         # display_statistics(filename)
          #sys.exit() """
  else:
      print "Usage : python get_community_graph.py -f <complete_graph_filename> -l <language> -s <Optional Language Statistics>"
      sys.exit()
  
  initializer(language,filename)
main()
