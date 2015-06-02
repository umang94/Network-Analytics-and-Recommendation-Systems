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
});

app.post('/trending', function(req, res){
	var language = req.body.language;
        console.log("language: " + language);
	var python = require('child_process').spawn('python', 
		// Array of parameters for the command python
		["/Users/umang/Desktop/MTP/Code/recommender.py",
		"-t", language]
		);
	python.stdout.on('data', function(data) {
		console.log('stdout: ' + data);
		res.header('Content-Type', 'application/json');
		res.send(200, data);
	});
	python.stderr.on('data', function(data) { console.log("stderr: " + data); });
});

app.post('/developers', function(req, res){
	var language = req.body.language,
	    user = req.body.user;
        console.log("language: " + language + ", user: " + user);
	var python = require('child_process').spawn('python', 
		// Array of parameters for the command python
		["/Users/umang/Desktop/MTP/Code/dev_recommender.py",
		"-u", user, "-l", language]
		);
	python.stdout.on('data', function(data) {
		console.log('stdout: ' + data);
		res.header('Content-Type', 'application/json');
		res.send(200, data);
	});
	python.stderr.on('data', function(data) { console.log("stderr: " + data); });
});

app.post('/developers/trending', function(req, res){
	var language = req.body.language;
        console.log("language: " + language);
	var python = require('child_process').spawn('python', 
		// Array of parameters for the command python
		["/Users/umang/Desktop/MTP/Code/dev_recommender.py",
		"-t", language]
		);
	python.stdout.on('data', function(data) {
		console.log('stdout: ' + data);
		res.header('Content-Type', 'application/json');
		res.send(200, data);
	});
	python.stderr.on('data', function(data) { console.log("stderr: " + data); });
});

app.listen(8888);
