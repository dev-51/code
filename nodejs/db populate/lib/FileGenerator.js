//*************************************************
//Get Modules
//*************************************************

var util = require("util")
	, EventEmitter = require('events').EventEmitter
	, fsIn = require('fs')
	, fsOut = require('fs')
	, StringType = require("./Types").Types.StringType;
	
//*************************************************
//Create Class
//*************************************************

var Class = function() { }
util.inherits(Class, EventEmitter);

//*************************************************
//Declare and implement methods
//*************************************************

Class.prototype.generate = function(filenameIn, filenameOut, delimiterColumn, delimiterRow, indexColumn, encoding="utf8") {
	var ob_this = this;
	
	fsIn.readFile(filenameIn, encoding, function(err, data) {
		if (err) throw err;

		lines = data.split(delimiterRow);
		var rowsOut = [];
		
		for (var index = 0; index < lines.length; index ++)
		{
			line = new StringType(lines[index]);
			rowsOut.push(line.trim().split(delimiterColumn)[indexColumn]);
		}

		fsOut.appendFile(filenameOut, rowsOut.join(delimiterRow), function (err) {
			if (err) throw err;
			
			//emit event
			ob_this.emit("onExecute_Generate", {inputFileName: filenameIn, outputFileName: filenameOut});				
		});
	});
};

//*************************************************
//Export Class
//*************************************************

module.exports = Class;
