import igraph
import random,sys
import json

def load_graph(filename):
    g = igraph.read(filename)
    return g

def test():
    community_graph = load_graph("Communities/C++.gml")
    for node in community_graph.vs:
        if len(node.neighbors()) > 0 : print node['name'], node['watchers'], node['label']

def search_node(query_repository, language_graph):
    for node in language_graph.vs:
        if node['label'] == query_repository:
            return node
    return None

def far_off_suggestions(language_graph, number): 
    page_ranks = language_graph.pagerank()
    pagerank_map = {}
    #for index in range(len(page_ranks)) : 
    #    pagerank_map[index] = [page_ranks[index],language_graph.vs[index]['watchers']]
    #x = sorted(pagerank_map.items(), key=lambda e: e[1][0], reverse=True)
    #print x
    for index in range(len(page_ranks)):
        pagerank_map[index] = page_ranks[index]
    top_repos = sorted(pagerank_map.items(),key=lambda e: e[1], reverse=True)[0:25]
    random.shuffle(top_repos)
    suggestions = []
    for id in top_repos:
        suggestions.append(language_graph.vs[id]['name'][0])
    return suggestions[0:number]


def make_json(suggestions):
    suggestions_map = {}
    for rank in range(1,11):
        suggestions_map[rank] = suggestions[rank-1]
    suggestions_json = json.dumps(suggestions_map)
    print suggestions_json

# Main recommender function that calls all the other auxillarily recommendor functions
def recommender(query_repository , language):
    
    #Loading the given language file
    language_file = "Communities/" + language + ".gml"
    language_graph = load_graph(language_file)

    #Searching the given repository in the logs
    root_node = search_node(query_repository, language_graph)
    
    if root_node is None :
        print "Sorry the given repository cannot be found in the logs"
        sys.exit()

    #Looking in the order = 2 neighboorhood
    neighborhood_node_ids = language_graph.neighborhood(int(root_node['id']),order=2)

    #Fetching suggested repository names and appendings suggestions rank wise

    suggestions = []
    for id in neighborhood_node_ids : 
        suggestions.append(language_graph.vs[id]['name'])
    if len(suggestions) < 10:
        suggestions = suggestions + far_off_suggestions(language_graph, 10-len(suggestions))

    for suggestion in suggestions:
        print suggestion
    

    make_json(suggestions)
    #ranks = community_graph.personalized_pagerank()
    #print sorted(ranks)
    #for node in community_graph.vs:
    #    if len(node.neighbors()) > 0 : print len(node.neighbors())

print "\t\tFor a independent node"
recommender("treeio/treeio","Python")

print "\t\tFor a connected node"
recommender("pydata/pandas", "Python")

print "\t\tFor a C++ independent node"
recommender("facebook/folly", "C++")

print "\t\tFor a C++ connected node"
recommender("facebook/hhvm", "C++")
