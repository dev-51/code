//*************************************************
//Get Modules
//*************************************************

var util = require("util")
	, EventEmitter = require('events').EventEmitter
	, Types = require("./Types").Types
	, FileGenerator = require("./FileGenerator")
	, NameGenerator = require("./NameGenerator")
	, DatabaseManager = require("./DatabaseManager");

//*************************************************
//Global variables
//*************************************************

var DateType = Types.DateType;
var NumberType = Types.NumberType;
var StringType = Types.StringType;

//*************************************************
//Create Class
//*************************************************

var Class = function() { }
util.inherits(Class, EventEmitter);

//*************************************************
//Declare and implement methods
//*************************************************

Class.prototype.getMasterIdValues = function() {
	var ob_this = this;
	var r_usertype = [], r_speciality = [];
	
	ob_this.db_manager.connection.query("SELECT id FROM usertype", function (err, result) {
		if (err) throw err;
		r_usertype = result;
	});

	ob_this.db_manager.connection.query("SELECT id FROM speciality", function (err, result) {
		if (err) throw err;
		r_speciality = result;
		
		//emit event
		ob_this.emit("onExecute_GetMasterIdValues", { usertype: r_usertype, speciality: r_speciality});		
	});	
};

Class.prototype.getIdValues = function() {
	var ob_this = this;
	var r_intern = [], r_extern = [];
	
	ob_this.db_manager.connection.query("SELECT id FROM intern", function (err, result) {
		if (err) throw err;
		r_intern = result;
	});

	ob_this.db_manager.connection.query("SELECT id FROM extern", function (err, result) {
		if (err) throw err;
		r_extern = result;
		
		//emit event
		ob_this.emit("onExecute_GetIdValues", { intern: r_intern, extern: r_extern});		
	});	
};

Class.prototype.getShiftIntern = function() {
	var ob_this = this;
	var r_shiftintern = [];
		
	ob_this.db_manager.connection.query(
															"SELECT " +
															"id, weekday, timeon, timeoff, id_intern, time_interval " +
															"FROM shift_intern " + 
															"ORDER BY id_intern, weekday", function (err, result) {
		if (err) throw err;
		r_shiftintern = result;
		
		//emit event
		ob_this.emit("onExecute_GetShiftIntern", { shiftintern: r_shiftintern});
	});
};

Class.prototype.getShiftWeekday = function() {
	var ob_this = this;
	var r_shiftweekday= [];

	ob_this.db_manager.connection.query(
															"SELECT " +
															"s.id, s.weekday, s.time_start, s.time_end, s.id_intern, w.name, w.total " + 
															"FROM shift_weekday s " + 
															"INNER JOIN " + 
															"(" + 
															"	SELECT DAYNAME(weekday) AS name, COUNT(1) AS total " + 
															"	FROM shift_weekday GROUP BY DAYNAME(weekday) " + 
															") w " +
															"ON DAYNAME(s.weekday) = w.name " + 
															"ORDER BY s.id_intern, s.weekday", function (err, result) {
		if (err) throw err;
		r_shiftweekday = result;
		
		//emit event
		ob_this.emit("onExecute_GetShiftWeekday", { shiftweekday: r_shiftweekday});
	});
};

Class.prototype.InsertSpeciality = function() {
	var ob_this = this;
	let rows = [];
		
	rows.push(["Pediatría"]);
	rows.push(["Otorrino"]);
	rows.push(["Infectología"]);
	rows.push(["Ginecología"]);
	rows.push(["Flebología"]);
	rows.push(["Cardiología"]);
		
	ob_this.db_manager.insert(
		"speciality"
	,	["name"]
	,	[rows]
	);	
};

Class.prototype.InsertUserType = function() {
	var ob_this = this;
	let rows = [];
		
	rows.push(["Administrador"]);
	rows.push(["Sistema"]);
	rows.push(["Interno"]);
		
	ob_this.db_manager.insert(
		"usertype"
	,	["name"]
	,	[rows]
	);	
};

Class.prototype.InsertIntern = function(data) {
	var ob_this = this;
	
	let rows = [];
	let num = new NumberType();
	let str = new StringType();
	
	let usertype = ob_this.dataCollection.usertype;
	let range = num.build_group(data.length, usertype.length);
	
	let list_usertype = [];
	let x = 0;
		
	range.forEach(function(item) {
		item.forEach(function(value) {
			list_usertype.push(usertype[x].id);
		});
		x ++;
	});
	
	x = 0;	
	data.forEach(function(item) {			
		rows.push([
			str.auto_generate_code()
		,	item[0]
		,	item[1]
		,	str.auto_generate_email(item[0], item[1])
		,	num.rnd_phone()
		,	num.rnd_mobile()
		,	str.auto_generate_username(item[0], item[1])
		,	"12345"
		,	list_usertype[x]
		]);
		x ++;
	});

	ob_this.db_manager.insert(
		"intern"
	,	["code", "name", "surname", "email", "phone", "mobile", "username", "password", "id_usertype"]
	,	[rows]
	);
};

Class.prototype.InsertExtern = function(data) {
	var ob_this = this;
	
	let rows = [];
	let num = new NumberType();
	let str = new StringType();
			
	data.forEach(function(item) {			
		rows.push([
			item[0]
		,	item[1]
		,	num.rnd_cardid()
		,	str.auto_generate_email(item[0], item[1])
		,	num.rnd_phone()
		]);
	});

	ob_this.db_manager.insert(
		"extern"
	,	["name", "surname", "cardid", "email", "phone"]
	,	[rows]
	);
};

Class.prototype.InsertShiftIntern = function() {
	var ob_this = this;
	let num = new NumberType();
	let date = new DateType();
	let intern = ob_this.dataCollection.intern;
	let speciality = ob_this.dataCollection.speciality;	
	let rows = [];
	
	let range = num.build_group(intern.length, speciality.length);	
	let list_speciality = [];
	let x = 0;
		
	range.forEach(function(item) {
		item.forEach(function(value) {
			list_speciality.push(speciality[x].id);
		});
		x ++;
	});
	
	x = 0;			
	intern.forEach(function(item) {			
		let days = date.weekdays();
		const timeon = "10:00";
		const timeoff = "18:00";
		let price = num.rnd_price();
		let time_interval = num.rnd_interval();
		
		days.forEach(function(day) {
			rows.push([
				date.format(day)
			,	timeon
			,	timeoff
			,	list_speciality[x]
			,	item.id
			,	price
			,	time_interval
			]);
		});
		
		x ++;
	});

	ob_this.db_manager.insert(
		"shift_intern"
	,	["weekday", "timeon", "timeoff", "id_speciality", "id_intern", "price", "time_interval"]
	,	[rows]
	);		
};

Class.prototype.InsertShiftExtern = function() {
	var ob_this = this;
	let intern = ob_this.dataCollection.intern;
	let extern = ob_this.dataCollection.extern;
	let swday = ob_this.dataCollection.shiftweekday;	
	let num = new NumberType();
	let date = new DateType();	
	let rows = [];		
	
	let weekdays = date.monthdays();
		
	weekdays.forEach(function(weekday) {
		let dayname = date.weeknames();
		let index = 0;				
		let id_extern = 0;
		const confirm = 1;
		let count = 0;
		let len = 0;
		let values = [];				
		
		swday.forEach(function(item) {	
			if (dayname[item.weekday.getDay()] == dayname[weekday.getDay()]) { //match same day
				if (count == 0) {
					len = Math.ceil(item.total / 2) + Math.floor(item.total / 3);
					values = num.rnd_listnum({"from": 0, "to": item.total - 1}, len);
				}				

				values.forEach(function(value) {	
					if (count == value) { //match all count value equals to any value of values array
						index = num.rnd_int(extern.length - 1, 0);
						id_extern = extern[index].id;

						rows.push([
							item.id_intern	
						,	id_extern
						,	date.format(item.weekday)
						,	item.time_start
						,	item.time_end
						,	confirm
						]);
						
						return;	
					}
				});
				
				count ++;
			} else {
				count = 0;
			}
		});
	});
	
	ob_this.db_manager.insert(
		"shift_extern"
	,	["id_intern", "id_extern", "weekday", "time_start", "time_end", "confirm"]
	,	[rows]
	);		
};

Class.prototype.InsertShiftWeekday = function() {
	var ob_this = this;
	let shiftintern = ob_this.dataCollection.shiftintern;
	let rows = [];
	let date = new DateType();
	
	shiftintern.forEach(function(item) {
		let timeon = item.timeon.split(":");
		let timeoff = item.timeoff.split(":");
		let shifts = date.shifts(
			timeon[0] + ":" + timeon[1]
		,	timeoff[0] + ":" + timeoff[1]
		,	item.time_interval
		);
		
		shifts.forEach(function(shift) {
			rows.push([
				item.id_intern
			,	date.format(item.weekday)
			,	shift[0]
			,	shift[1]
			]);			
		});			
	});	
	
	ob_this.db_manager.insert(
		"shift_weekday"
	,	["id_intern", "weekday", "time_start", "time_end"]
	,	[rows]
	);			
}

Class.prototype.generateOutputFiles = function() {
	var ob_this = this;

	ob_this.file_generator.generate(
		ob_this.dataCollection.files.nameMan.inputFilename
	,	ob_this.dataCollection.files.nameMan.outputFilename
	,	":"
	,	"\r\n"
	,	0
	);

	ob_this.file_generator.generate(
		ob_this.dataCollection.files.nameWoman.inputFilename 
	,	ob_this.dataCollection.files.nameWoman.outputFilename 
	,	":"
	,	"\r\n"
	,	0
	);
	
	ob_this.file_generator.generate(
		ob_this.dataCollection.files.surname.inputFilename
	,	ob_this.dataCollection.files.surname.outputFilename
	,	" \t"
	,	"\r\n"
	,	1
	);
};

Class.prototype.Exit = function() {
	var ob_this = this;
	ob_this.db_manager.close();	
	ob_this.emit("onExecute_Exit", {exitcode: 0});
};
			
Class.prototype.Main = function() {
	var ob_this = this;
	
	ob_this.dataCollection = {};	
	ob_this.db_manager = new DatabaseManager();
	ob_this.file_generator = new FileGenerator();
	ob_this.nm_generator = new NameGenerator();

	let files = {};	
	files.nameMan = {};
	files.nameMan.inputFilename = "./files/input/NameMan.txt";
	files.nameMan.outputFilename = "./files/output/NameManOut.txt";
	files.nameWoman = {};
	files.nameWoman.inputFilename = "./files/input/NameWoman.txt";
	files.nameWoman.outputFilename = "./files/output/NameWomanOut.txt";
	files.surname = {};
	files.surname.inputFilename = "./files/input/Surname.txt";
	files.surname.outputFilename = "./files/output/SurnameOut.txt";	
	ob_this.dataCollection.files = files;
			
	ob_this.db_manager.createConnection(
		"localhost"
	,	"username***"
	,	"password***"
	,	"databasename***"
	);

	ob_this.db_manager.open();	
			
	console.log("Generating output files ...");	
	ob_this.generateOutputFiles();	

	ob_this.file_generator.on("onExecute_Generate", function(data) {
		//last file generated
		if (data.outputFileName == files.surname.outputFilename) {
			//generate array of names for men and women
			console.log("Building full names for men and women ...");			
			ob_this.nm_generator.generate(
				ob_this.dataCollection.files.nameMan.outputFilename
			,	ob_this.dataCollection.files.nameWoman.outputFilename
			,	ob_this.dataCollection.files.surname.outputFilename
			,	"\r\n"
			);			
		}
	});
		
	ob_this.nm_generator.on("onExecute_Generate", function(data) {
		//get list of names generated
		ob_this.dataCollection.fullnames = data.fullnames;		
		
		console.log("Starting populating tables ...");
		
		//load master tables
		ob_this.InsertSpeciality();
		ob_this.InsertUserType();
		
		//get id from master tables
		ob_this.getMasterIdValues();		
	});
	
	ob_this.db_manager.on("onExecute_Insert", function(data) {
		console.log("Table Name: " + String(data.TableName));
		console.log("Inserted Rows: " + String(data.affectedRows));
		
		//previous to last tables inserted
		if (data.TableName == "extern") {
			ob_this.getIdValues();
		}
		
		//previous to last tables inserted
		if (data.TableName == "shift_intern") {
			ob_this.getShiftIntern();
		}
		
		//previous to last tables inserted
		if (data.TableName == "shift_weekday") {			
			ob_this.getShiftWeekday();
		}
		
		//last table inserted along the process
		if (data.TableName == "shift_extern") {
			//exit the process
			ob_this.Exit();
		}		
	});
	
	ob_this.on("onExecute_GetMasterIdValues", function(data) {
		//get id from master tables
		ob_this.dataCollection.usertype = data.usertype;
		ob_this.dataCollection.speciality = data.speciality;
		
		//separate list of names into 2 groups
		let fullnames = ob_this.dataCollection.fullnames;
		let num = new NumberType();		
		let range = num.build_group(fullnames.length, 2);
		let internNames = [], externNames = [];
		
		let x = 0;
		fullnames.forEach(function(item) {
			if (x <= range[0][range[0].length - 1]) {
				internNames.push(item);
			}
			
			if (x >= range[1][0]) {
				externNames.push(item);
			}
			x ++;
		});
		
		//add intern and extern records
		ob_this.InsertIntern(internNames);
		ob_this.InsertExtern(externNames);
	});	
	
	ob_this.on("onExecute_GetIdValues", function(data) {
		ob_this.dataCollection.intern = data.intern;
		ob_this.dataCollection.extern = data.extern;
		
		//add shift intern records
		ob_this.InsertShiftIntern();			
	});
	
	ob_this.on("onExecute_GetShiftIntern", function(data) {
		ob_this.dataCollection.shiftintern = data.shiftintern;
		
		//add shift weekday records
		ob_this.InsertShiftWeekday();
	});

	ob_this.on("onExecute_GetShiftWeekday", function(data) {
		ob_this.dataCollection.shiftweekday = data.shiftweekday;
		
		//add shift extern records
		ob_this.InsertShiftExtern();
	});	
	
	ob_this.on("onExecute_Exit", function(data) {
		console.log("\nProcess completed.\n");
		process.exit(data.exitcode);
	});	
};

//*************************************************
//Export Class
//*************************************************

module.exports = Class;
