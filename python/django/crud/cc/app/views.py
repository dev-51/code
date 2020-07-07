# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .createdb import restoreDatabase
from .actions import execAction
from .reader import getData, getRows
from .collector import createJSON

@csrf_exempt
def index(request):
    params = createJSON(request=request)
    message = execAction(params)
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
    def get(self, request, **kwargs):
        keys = [str(key) for key in kwargs]
        data = {}
        params = {}

        if len(keys):
            params = createJSON(arguments=kwargs)
        else:
            params = createJSON(request=request)

        keys = [str(key) for key in params]

        if 'insert' in keys or 'update' in keys or 'remove' in keys:
            message = execAction(params, True)
            data = {"message": message} if message else {"message": "done"}
        elif 'restore' in keys:
            restoreDatabase()
            data = {"message": "done"}
        elif 'view' in keys or 'show' in keys:
            data = {
                "data": getData(
                    cuit=params["cuit"],
                    account_type=params["account_type"],
                    rest_api=True
                )
            }
        elif 'list' in keys:
            data = {"data": getRows()}

        return Response(data)