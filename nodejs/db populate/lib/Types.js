//*************************************************
//Declare and implement methods [String Native Type]
//*************************************************

String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g,"");
}

String.prototype.ltrim = function() {
	return this.replace(/^\s+/,"");
}

String.prototype.rtrim = function() {
	return this.replace(/\s+$/,"");
}

String.prototype.auto_generate_code = function() {
	let value = [
		String.fromCharCode(Number.parseInt(Math.random() * (91 - 65) + 65))
	,	String.fromCharCode(Number.parseInt(Math.random() * (91 - 65) + 65))
	,	String.fromCharCode(Number.parseInt(Math.random() * (91 - 65) + 65))
	,	Number.parseInt(Math.random() * (1000 - 100) + 100)
	];
	
	return value.join("");
};

String.prototype.auto_generate_email = function(name, surname) {
	let index = Number.parseInt(Math.random() * (4 - 0) + 0);
	let fullname = name + " " + surname;
	
	fullname = fullname
		.replace(/ñ/gi, "n")
		.replace(/ü/gi, "u")
		.replace(/á/gi, "a")
		.replace(/é/gi, "e")
		.replace(/í/gi, "i")
		.replace(/ó/gi, "o")
		.replace(/ú/gi, "u");
			
	let value = [
		name.substr(0,1)
	,	fullname.substr(fullname.lastIndexOf(" ")+1, fullname.length)
	,	"@"
	,	["outlook.com", "hotmail.com", "gmail.com", "yahoo.com"][index]	
	];
	
	return value.join("").toLowerCase();
};

String.prototype.auto_generate_username = function(name, surname) {
	let fullname = name + " " + surname;
	
	fullname = fullname
		.replace(/ñ/gi, "n")
		.replace(/ü/gi, "u")
		.replace(/á/gi, "a")
		.replace(/é/gi, "e")
		.replace(/í/gi, "i")
		.replace(/ó/gi, "o")
		.replace(/ú/gi, "u");
		
	let value = [
		name.substr(0,1)
	,	fullname.substr(fullname.lastIndexOf(" ")+1, fullname.length)
	,	Number.parseInt(Math.random() * (100 - 10) + 10)
	];
	
	return value.join("").toLowerCase();
};

//*************************************************
//Declare and implement methods [Number Native Type]
//*************************************************
	
Number.prototype.rnd_int = function(max, min) {
	let random = Math.random() * ((max + 1) - min) + min;	
	return Number.parseInt(random);
};

Number.prototype.rnd_cardid = function() {
	let value = [
		Number.parseInt(Math.random() * (29 - 20) + 20)
	,	Number.parseInt(Math.random() * (1000 - 100) + 100)
	,	Number.parseInt(Math.random() * (1000 - 100) + 100)
	];
	
	return value.join("")
};

Number.prototype.rnd_phone = function() {
	let value = [
		4
	,	Number.parseInt(Math.random() * (3999 - 3000) + 3000)
	,	Number.parseInt(Math.random() * (1999 - 1000) + 1000)
	];
	
	return value.join("");
};

Number.prototype.rnd_mobile = function() {
	let value = [
		11
	,	Number.parseInt(Math.random() * (4999 - 4000) + 4000)
	,	Number.parseInt(Math.random() * (1999 - 1000) + 1000)
	];
	
	return value.join("");
};

Number.prototype.rnd_price = function() {
	let price = [600, 650, 700, 750, 800, 900, 1000];	
	let index = Number.parseInt(Math.random() * (price.length - 0) + 0);	
	return price[index];
};

Number.prototype.rnd_interval = function() {
	let interval = [15, 20, 30, 45];
	let index = Number.parseInt(Math.random() * (interval.length - 0) + 0);	
	return interval[index];
};

Number.prototype.get_interval = function() {
	return [15, 20, 30, 45];
};

Number.prototype.build_group = function(length, numParts) {
	let max = Number.parseInt(length / (numParts - 1)) - 1;
	let num = 0, count = 0, numStart = 0, numEnd = 0;
	let arr = [], sub_arr = [], value = [];
	let exit_loop = false;
	
	while(true) {
		num = Number.parseInt(Math.random() * (max - 1) + 1);
		
		if (arr.length == 0) {
			numStart = 0;
			numEnd = num;
		} else {
			value = arr[arr.length - 1];
			numStart = value[value.length - 1] + 1;
			
			if (count == numParts - 1){
				numEnd = length - 1;
				exit_loop = true;
			} else {						
				numEnd = (numStart + num) - 1;
			}
		}
		
		sub_arr = [];
		for(var x = numStart; x <= numEnd; x ++){
			sub_arr.push(x);
		}
		
		arr.push(sub_arr);
		count ++;
		
		if (exit_loop) break;
	}
	
	return arr;
};

Number.prototype.pad = function(size) {
    var s = String(this);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
};

//example: range={"from": 1, "to": 10}, length=5
Number.prototype.rnd_listnum = function(range, length) {
	let list = [];
	let count = 0;
	
	while (count < length) {
		list.push(Number.parseInt(Math.random() * ((range.to + 1) - range.from) + range.from));	
		count ++;
	}
	
	unique_items = list.filter(function(item, pos) {
		return list.indexOf(item) == pos;
	});
	
	return unique_items;
};

Date.prototype.weekdays = function(){
	let days =['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	let list = new Array(5);
	let cur_date = new Date();
	
	let index_monday = 1; //Monday
	let index_curday = cur_date.getDay();
		
	let diff = index_monday - ((index_curday == 0) ? 7:index_curday);
	let date_diff = cur_date.getDate() + diff;
	
	cur_date.setDate(date_diff);
	
	let monday = cur_date;
	let sum = 0;
	
	while(sum < 5) {
		let nextday = new Date(monday);
		let date_diff = nextday.getDate() + sum;
		
		nextday.setDate(date_diff);
		list.push(new Date(nextday));
		sum ++;
	}
		
	return list;	//return dates from Monday to Friday 
}

Date.prototype.format = function(date) {
	let value = [
		date.getFullYear()
	,	(date.getMonth() + 1).pad(2)
	,	(date.getDate()).pad(2)
	];
	
	return value.join("-");
};

Date.prototype.weeknames = function(){
	return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
};

Date.prototype.monthdays = function(){
	let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	let list = new Array(21);
	let count = 0;
	
	while(count < 31) {
		let date = new Date();	 //current date
		let diff = date.getDate() + count;
		let newdate = new Date(date.setDate(diff));
		
		if 
		(
			!(days[newdate.getDay()] == "Saturday" || days[newdate.getDay()] == "Sunday")
		) {
			list.push(newdate);	
		}
		
		count ++;		
	}
	
	return list;	//return weekdays for a month
}

Date.prototype.shifts = function(fromTime, toTime, interval){
	let list = [], pair = [];
	let arrFromTime = fromTime.split(":");
	let arrToTime = toTime.split(":");
	let dateFrom = new Date(2020, 5, 15, Number(arrFromTime[0]), Number(arrFromTime[1]), 0, 0);
	let dateTo = new Date(2020, 5, 15, Number(arrToTime[0]), Number(arrToTime[1]), 0, 0);
	let count = 0;
	
	while(true) {
		if (dateFrom > dateTo) break;
		
		count ++;		
		pair.push
		(
			Number(dateFrom.getHours()).pad(2) + ":" + Number(dateFrom.getMinutes()).pad(2)
		);
						
		dateFrom.setMinutes(dateFrom.getMinutes() + interval);
		
		if (count % 2 == 0) {
			list.push(pair);
			pair = [pair[pair.length - 1]];
			count = 1;
		}
	}
	
	return list;
}

         
//*************************************************
//Export Class
//*************************************************

module.exports = {
	Types: {
		StringType: String
	,	NumberType: Number
	,	DateType: Date
	}
};

