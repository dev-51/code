# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import defaults
from django.http import response
from django.core.exceptions import MultipleObjectsReturned
from .models import Account, Person, Company
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .database import Database
from .createdb import restoreDatabase

def commitInsert(r):
	db = Database(r.POST["cuit"], r.POST["account_type"])

	if r.POST["account_type"] == "F":
		db.insertPerson({
			"name": r.POST["name"],
			"surname": r.POST["surname"],
			"cardid": r.POST["cardid"]
		})
	elif r.POST["account_type"] == "J":
		db.insertCompany({
			"name": r.POST["name"],
			"year": r.POST["year"]
		})

def commitUpdate(r):
	db = Database(r.POST["cuit"], r.POST["account_type"])

	if r.POST["account_type"] == "F":
		db.updatePerson({
			"name": r.POST["name"],
			"surname": r.POST["surname"],
			"cardid": r.POST["cardid"]
		})
	elif r.POST["account_type"] == "J":
		db.updateCompany({
			"name": r.POST["name"],
			"year": r.POST["year"]
		})

def commitRemove(r):
	db = Database(r.POST["cuit"], r.POST["account_type"])

	if r.POST["account_type"] == "F":
		db.removePerson()
	elif r.POST["account_type"] == "J":
		db.removeCompany()

def execAction(r):
	keys = [str(key) for key in r.POST.iterkeys()]
	pre_error = None

	if "insert" in keys:
		count = Account.objects.filter(cuit=r.POST["cuit"]).count()
		if count > 0:
			pre_error = \
				"""
				Ya existe el mismo número de cuit {}. 
				Por lo tanto, no ha sido insertado a la 
				base de datos.
				""".format(r.POST["cuit"])
		else:
			commitInsert(r)
	elif "update" in keys:
		count = Account.objects.filter(cuit=r.POST["cuit"]).count()
		if count > 1:
			pre_error = \
				"""
				Atención: El número de cuit {} existe más de una vez. 
				La operación de grabar en base de datos, ha sido cancelada.
				""".format(r.POST["cuit"])
		else:
			commitUpdate(r)
	elif "remove" in keys:
		count = Account.objects.filter(cuit=r.POST["cuit"]).count()
		if count > 1:
			pre_error = \
				"""
				Atención: El número de cuit {} existe más de una vez. 
				La operación de borrar en base de datos, ha sido cancelada.
				""".format(r.POST["cuit"])
		else:
			commitRemove(r)

	return pre_error

def getData(request, cuit, account_type):
	data = {}
	account = None

	try:
		account = Account.objects.get(cuit=cuit)
	except (MultipleObjectsReturned) as e:
		data = {
			"error":
				"""
				Lo siento, pero ha ocurrido un error al obtener un 
				registro con el mismo número de cuit.
				"""
		}

	if account:
		if account_type == "F":
			data = {
				"error": None,
				"person": Person.objects.get(account=account),
				"account_type": account_type
			}
		elif account_type == "J":
			data = {
				"error": None,
				"company": Company.objects.get(account=account),
				"account_type": account_type
			}

	return data

@csrf_exempt
def index(request):
	message_error = execAction(request)

	all_accounts = Account.objects.all()
	len_accounts = Account.objects.count()
	list = []

	if len_accounts:
		for account in all_accounts:
			if account.account_type == "F":
				person = Person.objects.get(account=account)
				list.append({
					"cuit": account.cuit,
					"cuit_label": str(account.cuit)[:2] + "-" + str(account.cuit)[2:10] + "-" + str(account.cuit)[-1:],
					"name": person.name + " " + person.surname,
					"account_type": account.account_type
				})
			elif account.account_type == "J":
				company = Company.objects.get(account=account)
				list.append({
					"cuit": account.cuit,
					"cuit_label": str(account.cuit)[:2] + "-" + str(account.cuit)[2:10] + "-" + str(account.cuit)[-1:],
					"name": company.name,
					"account_type": account.account_type
				})

	return render(
		request,
		"app/index.html",
		{"all_accounts": list, "message_error": message_error}
	)

@csrf_exempt
def create(request):
	restoreDatabase()
	return render(request, "app/createdb.html", {})

@csrf_exempt
def add(request, account_type):
	return render(request, "app/add.html", {"account_type": account_type})

@csrf_exempt
def edit(request, cuit, account_type):
	data = getData(request, cuit, account_type)
	return render(request, "app/edit.html", {"data": data})

@csrf_exempt
def remove(request, cuit, account_type):
	data = getData(request, cuit, account_type)
	return render(request, "app/remove.html", {"data": data})

@csrf_exempt
def view(request, cuit, account_type):
	data = getData(request, cuit, account_type)
	return render(request, "app/view.html", {"data": data})

