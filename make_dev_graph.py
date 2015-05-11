#!usr/bin/env python

""" Code for generating developer graph by reading raw_data from a csv file """ 
import csv, igraph

g = igraph.Graph()

repo_developer_map = {}

# Code for extracting deelopers and adding unique nodes correspoding to each developer into the graph

developers_set = set()
with open('developer_data/Python.csv', 'rb') as devfile:
    reader = csv.DictReader(devfile)
    for dev in reader:
        if dev['actor_attributes_name'] not in developers_set:
            developers_set.add(dev['actor_attributes_name'])
            g.add_vertex(name=dev['actor_attributes_name'],
                label=dev['actor'],
                language=dev['repository_language'],
                email=dev['actor_attributes_email'])
        
        if dev['repository_name'] not in repo_developer_map:
            repo_developer_map[dev['repository_name']] = {dev['actor_attributes_name']:1}
            #print repo_developer_map['repository_name'] , "Added"
        elif dev['repository_name'] in repo_developer_map:
            if dev['actor_attributes_name'] in repo_developer_map[dev['repository_name']]:
                repo_developer_map[dev['repository_name']][dev['actor_attributes_name']] += 1
                #print repo_developer_map[dev['repository_name']][dev['actor_attributes_name']], "Updated"
            else:
                repo_developer_map[dev['repository_name']][dev['actor_attributes_name']] = 1
                #print repo_developer_map[dev['repository_name']][dev['actor_attributes_name']], "Updated"

print "Node generation complete ... "
print "Repository Developer Map genration complete ..." 
print "Starting Edge Generation ..."

#for repsoitory, developers in repo_developer_map.items():
#    for developer, contribution in developers.items():
 
#igraph.plot(g)




# Code for processing the information regarding edges in the graph 



#g.write("Python.gml")


