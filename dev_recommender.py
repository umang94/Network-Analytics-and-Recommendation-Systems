import igraph, random, sys, json

#Function to load graph file
def load_graph(language):
    filename = "/Users/umang/Desktop/MTP/Code/developer_graphs/" + language + ".gml"
    g=igraph.read(filename)
    return g

#Function to search for a given node in the user graph
def search_node(developer_username,developer_graph):
    for node in developer_graph.vs:
        if node['label'] == developer_username:
            return node
    return None

#Function for filtering out top developers who do not have any edges. This is for adding granularity to the recommendations

def independent_suggestions(developer_graph,number):
    independent_developers = []
    for node in developer_graph.vs:
        Name = node['name']
        Email = node['email']
        Username = node['label']
        if len(node.neighbors()) == 0 and node['email'] != 'null':
            if Name == '' or Name == 'null':
                Name = "Not Available"
            if Email == '' or Email == 'null':
                Email = "Not Available"
            if Username == '' or Username == 'null':
                ProfileLink = "Not Available"
            else:
                ProfileLink = "github.com/" + Username 

            independent_developers.append([Name,Email,ProfileLink])
    random.shuffle(independent_developers)
    return independent_developers[0:number]

#Returning top ranked developers in the given language community. Format of return array is 
# [[developer_name1, developer_email1, developer_username1], [developer_name2, developer_email2, developer_username2]]

def ranked_suggestions(developer_graph,number):
    page_ranks = developer_graph.pagerank()
    pagerank_map = {}
    for index in range(len(page_ranks)):
        pagerank_map[index] = page_ranks[index]
    top_developers = sorted(pagerank_map.items(), key=lambda e:e[1], reverse=True)
    suggestions = []
    for id in top_developers:
        Name = developer_graph.vs[id]['name'][0]
        Email = developer_graph.vs[id]['email'][0]
        Username = developer_graph.vs[id]['label'][0]
        if Name == '' or Name == 'null':
            Name = "Not Available"
        if Email == '' or Email == 'null':
            Email = "Not Available"
        if Username == '' or Username == 'null':
            ProfileLink = "Not Available"
        else:
            ProfileLink = "github.com/" + Username 
        suggestions.append([Name, Email, ProfileLink])
    return suggestions[0:number]


def recommender(developer_username, language):
    #Loading the given developer_graph corresponding to the langauge
    developer_graph = load_graph(language) 
    root_node = search_node(developer_username,developer_graph)
    if root_node is None:
        return ranked_suggestions(developer_graph,10) + independent_suggestions(developer_graph,10)
        #Adding a mixture of independent and ranked suggestions here 

    #Order 2 neighborhood recommendation
    neighbors_node_ids = developer_graph.neighborhood(int(root_node['id']), order=2)

    #fetching the suggestions 

    suggestions = []
    for id in neighbors_node_ids:
        Name = developer_graph.vs[id]['name']
        Email = developer_graph.vs[id]['email']
        Username = developer_graph.vs[id]['label']
        if Name == '' or Name == 'null':
            Name = 'Not Available'
        if Email == '' or Email == 'null':
            Email = 'Not Available'
        if Username == '' or Username == 'null' : 
            ProfileLink = 'Not Available'
        else:
            ProfileLink = 'github.com/' + Username
        suggestions.append([Name, Email, ProfileLink])
    suggestions = suggestions[0:10] + ranked_suggestions(developer_graph,5) + independent_suggestions(developer_graph, 5)

    return json.dumps(suggestions)

print recommender("grayj",'Python')


