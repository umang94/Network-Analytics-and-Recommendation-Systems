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

app.use(express.static(__dirname + "/public"));

app.post('/', function(req, res){
	var language = req.body.language,
	    repository = req.body.repository;
        console.log("language: " + language + ", repo: " + repository);
	var python = require('child_process').spawn('python', 
		// Array of parameters for the command python
		["/Users/umang/Desktop/MTP/Code/recommender.py",
		"-r", repository, "-l", language]
		);
	python.stdout.on('data', function(data) {
		console.log('stdout: ' + data);
		res.header('Content-Type', 'application/json');
		res.send(200, data);
	});
	python.stderr.on('data', function(data) { console.log("stderr: " + data); });
	/*
	python.on('close', function(code){
		console.log("child process exited with code: " + code);
		if(code !== 0){return res.send(500,code);}
		return res.send(200, output)
	});*/
});
app.listen(8888);
