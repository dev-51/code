# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .createdb import restoreDatabase
from .actions import execAction
from .reader import getData, getRows

@csrf_exempt
def index(request):
	message = execAction(request)
	list = getRows()

	return render(
		request,
		"app/index.html",
		{
			"all_accounts": list,
			"message": message
		}
	)

@csrf_exempt
def restore(request):
	restoreDatabase()
	return render(request, "app/createdb.html", {})

@csrf_exempt
def add(request, account_type):
	return render(request, "app/add.html", {"account_type": account_type})

@csrf_exempt
def edit(request, cuit, account_type):
	data = getData(cuit, account_type)
	return render(request, "app/edit.html", {"data": data})

@csrf_exempt
def remove(request, cuit, account_type):
	data = getData(cuit, account_type)
	return render(request, "app/remove.html", {"data": data})

@csrf_exempt
def view(request, cuit, account_type):
	data = getData(cuit, account_type)
	return render(request, "app/view.html", {"data": data})

class CRUD(APIView):
	def get(self, request):
		keys = [str(key) for key in request.GET.iterkeys()]
		data = {}

		if 'insert' in keys or 'update' in keys or 'remove' in keys:
			message = execAction(request, True)
			data = {"message": message} if message else {"message": "done"}
		elif 'restore' in keys:
			restoreDatabase()
			data = {"message": "done"}
		elif 'view' in keys:
			data = {
				"data": getData(
					cuit=request.GET["cuit"],
					account_type=request.GET["account_type"],
					rest_api=True
				)
			}
		elif 'list' in keys:
			data = {"data": getRows()}

		return Response(data)
