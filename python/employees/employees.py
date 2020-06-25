#!/usr/bin/python2.7
import requests
import os
import json
import pprint
import sys

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#call examples
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#./employees.py/4?expand=manager
#./employees.py/4
#./employees.py?limit=3&offset=2&expand=department.superdepartment.superdepartment&expand=office
#./employees.py?expand=manager.manager.manager&expand=manager.office
#./employees.py/1?expand=office&expand=manager.manager.manager
#./employees.py?limit=1&offset=4
#./employees.py?limit=4
#

pp = pprint.PrettyPrinter(indent=5)

content = requests.get('http://localhost:8080/employees/employees.json')
employees = json.loads(content.text)

content = requests.get('http://localhost:8080/employees/offices.json')
offices = json.loads(content.text)

content = requests.get('http://localhost:8080/employees/departments.json')
departments = json.loads(content.text)

query_string = os.environ.get("QUERY_STRING", "")
path_info = os.environ.get("PATH_INFO", "")

request_method = os.environ.get("REQUEST_METHOD")
value_post = ""
if request_method == "POST":
	value_post = str(sys.stdin.read())

params = query_string.split("&")
limit = 100
offset = 0
limit_max = 1000
expand = []

emp_id_sel = None
if len(path_info):
	emp_id_sel = int(path_info[1:])
	
if limit > limit_max:
	limit = limit_max
		
for p in params:
	param = p.split("=")

	if param[0] == "limit":
		limit = int(param[1])
	elif param[0] == "offset":
		offset = int(param[1])
	elif param[0] == "expand":
		expand.append(param[1])
		
employees_all = []
count_all = 0
count = 0

for emp in employees:
	count_all += 1
	emp_id = int(emp["id"])
	
	if count_all > offset:
		count += 1
		
		if emp_id_sel == emp_id or (emp_id_sel is None and count <= limit):
			item = {}
			
			for name in emp.keys():
				if name not in ["department", "office", "manager"]:
					item[name] = emp[name]
			
			if "office" in expand:
				#open root/office
				item["office"] = None		
				for off in offices:
					if emp["office"] is not None and emp["office"] == off["id"]:
						item["office"] = off.copy()
			else:
				item["office"] = emp["office"]
			
			if "department" in expand or "department.superdepartment" in expand or "department.superdepartment.superdepartment" in expand:	
				#open root/department
				item["department"] = None
				for dep in departments:
					if emp["department"] is not None and emp["department"] == dep["id"]:
						item["department"] = dep.copy()
					
					#open root/department/superdepartment	
					if ("department.superdepartment" in expand or "department.superdepartment.superdepartment" in expand) and item["department"] is not None:				
						for dep in departments:
							if item["department"]["superdepartment"] is not None and item["department"]["superdepartment"] == dep["id"]:
								item["department"]["superdepartment"] = dep.copy()					
													
						#open root/department/superdepartment/superdepartment	
						if "department.superdepartment.superdepartment" in expand and item["department"]["superdepartment"] is not None:
							for dep in departments:
								if item["department"]["superdepartment"]["superdepartment"] is not None and item["department"]["superdepartment"]["superdepartment"] == dep["id"]:
									item["department"]["superdepartment"]["superdepartment"] = dep.copy()
			else:
				item["department"] = emp["department"]

			if "manager" in expand or "manager.manager" in expand or "manager.manager.manager" in expand or "manager.manager.office" in expand or "manager.office" in expand:
				#open root/manager
				item["manager"] = None
				for em in employees:
					if emp["manager"] is not None and emp["manager"] == em["id"]:
						item["manager"] = em.copy()
			else:
				item["manager"] = emp["manager"]
			
			if "manager.manager" in expand or "manager.manager.manager" in expand or "manager.manager.office" in expand or "manager.office" in expand:
				if "manager.manager" in expand or "manager.manager.manager" in expand or "manager.manager.office" in expand:
					#open root/manager/manager		
					if item["manager"] is not None:				
						for em in employees:
							if item["manager"]["manager"] is not None and item["manager"]["manager"] == em["id"]:
								item["manager"]["manager"] = em.copy() #to avoid using same chunk of memory
					
					if "manager.manager.manager" in expand:
						#open root/manager/manager/manager
						if item["manager"] is not None and item["manager"]["manager"] is not None:
							for em in employees:
								if item["manager"]["manager"]["manager"] is not None and item["manager"]["manager"]["manager"] == em["id"]:
									item["manager"]["manager"]["manager"] = em.copy()
								
					if "manager.manager.office" in expand:
						#open root/manager/manager/office
						if item["manager"] is not None and item["manager"]["manager"] is not None:
							for off in offices:
								if item["manager"]["manager"]["office"] is not None and item["manager"]["manager"]["office"] == off["id"]:
									item["manager"]["manager"]["office"] = off.copy()
					
				if "manager.office" in expand:
					#open root/manager/office
					for off in offices:
						if item["manager"] is not None and item["manager"]["office"] is not None and item["manager"]["office"] == off["id"]:
							item["manager"]["office"] = off.copy()
						
			employees_all.append(item)
			
			if emp_id_sel is not None:
				break
		else:
			if emp_id_sel is None:
				break #stop iterating employees rows		
						
print("Content-type: application/json")
print("")
#print(json.dumps(expand))
pp.pprint(employees_all)

