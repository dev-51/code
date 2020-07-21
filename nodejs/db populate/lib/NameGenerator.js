//*************************************************
//Get Modules
//*************************************************

var util = require("util")
	, EventEmitter = require('events').EventEmitter
	, fileMan = require("fs")
	, fileWoman = require("fs")
	, fileSurname = require("fs")
	, NumberType = require("./Types").Types.NumberType;

//*************************************************
//Create Class
//*************************************************

var Class = function() { }
util.inherits(Class, EventEmitter);

//*************************************************
//Declare and implement methods
//*************************************************

Class.prototype.generate = function(filenameNameMan, filenameNameWoman, filenameSurname, delimiterRow, encoding = "utf8") {
	var ob_this = this;
	
	var filenameMan = filenameNameMan
		, filenameWoman = filenameNameWoman
		, filenameSurname = filenameSurname;

	var rowsMan = []
		, rowsWoman = []
		, rowsSurname = [];
	
	//read files' content	
	fileMan.readFile(filenameMan, encoding, function(err, data) {
		if (err) throw err;
		rowsMan = data.split(delimiterRow);
	  
		fileWoman.readFile(filenameWoman, encoding, function(err, data) {
			if (err) throw err;
			rowsWoman = data.split(delimiterRow);
			
			fileSurname.readFile(filenameSurname, encoding, function(err, data) {
				if (err) throw err;
				rowsSurname = data.split(delimiterRow);

				let num = new NumberType();
				
				//men	construction			
				var men_name = new Array();
				var max = 99, min = 0, random = 0;
				
				for (var i = min; i <= max; i ++){
					let indexName0 = num.rnd_int(max, min);
					let indexName1 = num.rnd_int(max, min);
					let indexSurname = num.rnd_int(max, min);
	
					//man name
					let name = rowsMan[indexName0] + ' ' +rowsMan[indexName1];
					let surname = rowsSurname[indexSurname];				
					let man_name = new Array();
					
					if (surname.indexOf("/") != -1) {
						surname = surname.split("/")[0];
					}
					
					man_name.push(name);
					man_name.push(surname);
					man_name.push("M");
					
					men_name.push(man_name);							
				}
				
				//women construction
				var women_name = new Array();
				var max = 69, min = 0, random = 0;
				
				for (var i = min; i <= max; i ++){
					let indexName0 = num.rnd_int(max, min);
					let indexName1 = num.rnd_int(max, min);
					let indexSurname = num.rnd_int(max, min);

					//woman name
					let name = rowsWoman[indexName0] + ' ' +rowsWoman[indexName1];
					let surname = rowsSurname[indexSurname];
					let woman_name = new Array();
					
					if (surname.indexOf("/") != -1) {
						surname = surname.split("/")[0];
					}
					
					woman_name.push(name);
					woman_name.push(surname);
					woman_name.push("F");
					
					women_name.push(woman_name);							
				}
				
				//mix men and women records among each other
				var copy_arrA = null;
				var copy_arrB = null;
				
				if (men_name.length > women_name.length) {
					copy_arrA = men_name;
					copy_arrB = women_name;
				} else { 
					//women_name either has more or equal amount of elements than men_name
					copy_arrA = women_name;
					copy_arrB = men_name;
				}
				
				var mix_arr = [];	
				var i = 0;		
				var ii = 0;
				
				copy_arrA.forEach(function (item, index, arr) {				
					if (i < copy_arrB.length) {
						mix_arr.push(copy_arrB[i]);
						i ++;
					}

					if (ii < arr.length) {
						mix_arr.push(arr[ii]);
						ii ++;
					}				
				});

				//emit event
				ob_this.emit("onExecute_Generate", { fullnames: mix_arr });
			});					
		});			 
	});
};

//*************************************************
//Export Class
//*************************************************

module.exports = Class;

