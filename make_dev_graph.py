#!usr/bin/env python

""" Code for generating developer graph by reading raw_data from a csv file """ 
import csv, igraph, math, time




# Code for extracting deelopers and adding unique nodes correspoding to each developer into the graph

def construct_graph(language):
    start = time.clock()
    g = igraph.Graph()
    repo_developer_map = {}
    developers_set = set()
    raw_file = 'developer_data/' + language + '.csv'
    with open(raw_file, 'rb') as devfile:
        reader = csv.DictReader(devfile)
#Adding nodes in the graph
        for dev in reader:
            if dev['actor_attributes_name'] not in developers_set:
                developers_set.add(dev['actor_attributes_name'])
                g.add_vertex(name=dev['actor_attributes_name'],
                label=dev['actor'],
                language=dev['repository_language'],
                email=dev['actor_attributes_email'])
        
            if dev['repository_name'] not in repo_developer_map:
                repo_developer_map[dev['repository_name']] = {dev['actor_attributes_name']:1}
            elif dev['repository_name'] in repo_developer_map:
                if dev['actor_attributes_name'] in repo_developer_map[dev['repository_name']]:
                    repo_developer_map[dev['repository_name']][dev['actor_attributes_name']] += 1
                else:
                    repo_developer_map[dev['repository_name']][dev['actor_attributes_name']] = 1
#adding edges in the developer graph
    for repsoitory, developers in repo_developer_map.items():
        current_set = developers.items()
        for index1 in range(0,len(current_set)-1):
            for index2 in range(index1+1, len(current_set)):
                edge_weight = math.sqrt(current_set[index1][1] * current_set[index2][1])
                g.add_edge(current_set[index1][0], current_set[index2][0],weight=edge_weight)

# Code for processing the information regarding edges in the graph 
    output_file = 'developer_graphs/' + language + '.gml'
    g.write(output_file)
    end = time.clock()
    print output_file , "Written", '\t\t\t', end-start , 'seconds'


#Automation for creating developer graphs of the language communities 

languages = ['ActionScript', 'Assembly', 'C', 'C#', 'C++', 'Clojure', 'CoffeeScript', 'Dart', 
        'Elixir', 'Emacs Lisp' , 'Erlang' , 'Go' , 'Groovy' , 'Haskell' , 'Java' , 'JavaScript',
        'Julia', 'Matlab', 'Objective-C', 'OCaml' , 'Perl', 'PHP', 'PowerShell', 'Python', 'Ruby',
        'Rust', 'Scala', 'Shell', 'Vala', 'VimL', 'Visual Basic']

for language in languages:
    construct_graph(language)

#construct_graph('VimL')
