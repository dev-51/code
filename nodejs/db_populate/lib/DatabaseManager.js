//*************************************************
//Get Modules
//*************************************************

var mysql = require('mysql')
	, util = require("util")
	, EventEmitter = require('events').EventEmitter;

//*************************************************
//Create Class
//*************************************************

var Class = function() { }
util.inherits(Class, EventEmitter);

//*************************************************
//Declare and implement methods
//*************************************************

Class.prototype.createConnection = function(hostname, db_username, db_password, db_databasename) {
	var ob_this = this;
	
	ob_this.connection = mysql.createConnection({
		host: hostname
	,	user: db_username
	,	password: db_password
	,	database: db_databasename
	});
};

Class.prototype.open = function() {
	var ob_this = this;
	
	ob_this.connection.connect(function(err) {
		if (err) throw err;
	});	
};

Class.prototype.close = function() {
	var ob_this = this;
	
	ob_this.connection.end(function(err) {
		if (err) throw err;		
		ob_this.connection.destroy();
	});	
};

//Example: objectInstance.select("intern", ["name", "surname", "email"], [{id:73}, {surname:"Smith"}]);
Class.prototype.select = function(tablename, fields, condition = []){
	var ob_this = this;

	let sql_template = "SELECT " + fields.join(",") + " FROM " + tablename;
		
	if (condition.length) {
		sql_template += " WHERE ?";
		rows = condition;
	}
	
	ob_this.connection.query(sql_template, rows, function (err, result) {
		if (err) throw err;
		
		//emit event
		ob_this.emit("onExecute_Select", { TableName: tablename, Rows: result });
	});	
};

//Example: objectInstance.insert("intern"
//	, ["code", "name", "surname", "email", "phone", "mobile", "username", "password", "id_usertype"]
//	, [
//		[
//			["USR089", "John", "Doe", "jdoe@gmail.com", "457771111", "1147113333", "jdoe", "12345", 1]
//		,	["RFH878", "James", "Watt", "jwatt@gmail.com", "457772222", "1147114444", "jwatt", "12345", 1]
//		]
//	  ]
//	);
Class.prototype.insert = function(tablename, fields, rows){
	var ob_this = this;

	let sql_template = "INSERT INTO " + tablename + " (" + fields.join(",") + ")";
	sql_template += " VALUES ?";

	ob_this.connection.query(sql_template, rows, function (err, result) {
		if (err) throw err;
		
		//emit event
		ob_this.emit("onExecute_Insert", { TableName: tablename, affectedRows: result.affectedRows });
	});	
};

//Example: objectInstance.update("intern", {name:"John", surname:"Donne"}, {id:"143"});
Class.prototype.update = function(tablename, fields, condition = null){
	var ob_this = this;
	
	let rows = [];	
	let sql_template = "UPDATE " + tablename + " SET ?";
	
	rows.push(fields);
	
	if (condition) {
		sql_template += " WHERE ?";
		rows.push(condition);
	}
	
	ob_this.connection.query(sql_template, rows, function (err, result) {
		if (err) throw err;
		
		//emit event
		ob_this.emit("onExecute_Update", { TableName: tablename, affectedRows: result.affectedRows });
	});	
};

//Example: objectInstance.remove("intern", [{id:"142"}]);
Class.prototype.remove = function(tablename, condition = []){
	var ob_this = this;
	
	let sql_template = "DELETE FROM " + tablename;
	
	if (condition.length) {
		sql_template += " WHERE ?";
		rows = condition;
	}
	
	ob_this.connection.query(sql_template, rows, function (err, result) {
		if (err) throw err;
		
		//emit event
		ob_this.emit("onExecute_Remove", { TableName: tablename, affectedRows: result.affectedRows });
	});	
};

//*************************************************
//Export Class
//*************************************************
			  
module.exports = Class;

