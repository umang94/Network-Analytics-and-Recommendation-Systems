var express = require("express");
/* 
 * body-parser is a piece of express middleware that reads a form's input and stores it as a 
 * javascript object accessible through 'req.body'
 */
var bodyParser = require('body-parser');

//Creating app
var app = express();

// using bodyParser() middleware for all routes
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.get("/", function(req,res){
	//This is the function going to be executed when the browser requests a get on the
	//homepage
	
	var html = '<form action="/" method="post">' +
               'Enter the language: ' +
               '<input type="text" name="language" placeholder="..." />' +
               '<br>' +
	       'Enter the repository name : ' +
	       '<input type="text" name="repository" placeholder="..." />' + 
               '<button type="submit">Submit</button>' +
            '</form>';
	res.send(html);
});

app.post('/', function(req, res){
	var language = req.body.language;
	var repository = req.body.repository;
	var python = require('child_process').spawn('python', 
		// Array of parameters for the command python
		["~/Desktop/MTP/Code/recommender.py",
		"-r", repository, "-l", language]
		);
	var output = "";
	python.stdout.on('data', function(){console.log(data)});
	console.log("Works");
	console.log(output);
	python.on('close', function(code){
		if(code !== 0){return res.send(500,code);}
		return res.send(200, output)
	});
});
app.listen(8888);
