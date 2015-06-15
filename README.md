#Network Analytics and Recommendation System for GitHub Hosted Projects and Developers
A Recommendation system based on the Collaboration Network analysis of the projects hosted on GitHub and the active developers on GitHub. 

## Modules of the project

The project has two modules :

	* Recommendation Engine for Similar Projects 
	* Recommendation Engine for Similar Developers

##Overview of the Recommendation Engine

The data is mined from [GitHub Archive](http://githubarvhive.org). The data is then loaded on to [Google BigQuery](https://bigquery.cloud.google.com). SQL queries are used to extract the Network Graph data like nodes and edges. In case of the Collaboration Network of Projects, every Project is a node in the graph and the edges and their weights between any two nodes are calculated based on the contributions of the common developers between the two nodes. Similarly in case of the Collaboration Network of the Developers, the nodes are individual developers and the edges between any two nodes is calculated by considering the common repositories the two developers have worked on together. The contribution of a single common developer to the edge weight between two project nodes is given by the under-root of the product of the individual contribution made my the developer to both the projects separately. The individual contribution of a developer to a given repository is determined by the number of commits he has made to that repository. The processed under-root values are then summed up over the set of all common developers between two nodes to arrive at the final edge weight between the nodes in consideration. 

Once the collaboration network is formed, we build a Neighbourhood Filtering based Recommendation Engine on top of the Collaboration Network. An outline of the data flow and execution steps of the Recommendation Engine for similar Projects is as follows :

	1. The user enters the GitHub link to a repository and the main programming language used by the project. Mentioning the programming language helps us identify the community the project belongs too.
	2. The Recommendation System queries the Network analytics module and loads the collaboration network of the language inputted. 
	3. A search for the queried repository is made in this graph and on successful retreival of the corresponding node, the neighbourhood is extracted. 
	4. The neighbourhood nodes are further processed to get the GitHub links and small descriptions are sent out as output.

### Decomposition of the Recommendations 

The Recommendations made aren't entirely based on the neighbourhood of the queried node. This is because this would make the recommendations completely dependent on the how much the node is connected to the other nodes in the graph. This becomes a major limitation as the network analysis of GitHub projects and developers clearly shows how a majority of developer nodes and project nodes are completely independent. To overcome this limitation, we have tried to add granularity to the recommendations as follows 

	* Independent Suggestions : These suggestions incorporate the independent nodes in the graph. They are ranked based on the number of stars they have. 
	* Popular Suggestions : These suggestions comprise of the nodes that have high ranking after applying the undirected graph version of the PageRank algorithm
	* Neighbourhood Suggestions : The suggestions comprising of the nodes in the neighbourhood of the queried node

### What happens if the queried node is not present in the graph ? 

The recommendations then contain only the Independent Suggestions and Popular Suggestions. As simple as that !

### Tech Stack

* Primary Language :  [Python](https://www.python.org)
* Graphing Library :  [python-igraph](http://www.igraph.org/python/doc/igraph-module.html)
* Plotting : [R](http://cran.r-project.org/) , [gephi](http://www.github.gephi.io)
* Website : [Node.js](http://nodejs.org) , [Bootstrap](http://www.getbootstrap.com)

### Installation

The installation has to be done manually right now. 

* Install [Python](https://www.python.org) 
* Install [Igraph](http://igraph.org/python/doc/tutorial/install.html)
* Install [R](http://cran.r-project.org/)
* Install [Node.js](http://nodejs.org)
* Modify recommender.py , dev_recommender.py , make_graph.py, make_dev_graph.py to change the absolute address of the directories

### Running Instructions 

Some sample examples have been shown as below

For getting recommendations for similar projects 

    $ python recommender.py -r pydata/pandas -l python
    $ python recommender.py -r facebook/folly -l c++
    $ python recommender.py -r facebook/hhvm -l C++

For getting the trending repositories for a language

    $ python recommender.py -t python

For getting recommendations for similar developers

    $ python dev_recommender.py -u Fronx -l JavaScript
    $ python dev_recommender.py -u Liang -l C++

For getting the trending developers in a language community

    $ python dev_recommender.py -t Python

### Web Interface 

We have also set up a basic Node.js based website for the ease of usage and bypassing the command line instructions. The website can be reached at https://localhost:8888/ after initialising the server. The website files are located in the frontend/ folder and the server can be started as follows

	$ cd frontend
	$ node server.js
