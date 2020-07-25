# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from .createdb import restoreDatabase
from .actions import execAction
from .reader import getData, getRows
from .collector import createJSON

class IndexView(View):
    def __process(self, request):
        params = createJSON(request=request)
        message = execAction(params)
        list = getRows()

        return (list, message)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        result = self.__process(request)
        return render(
            request,
            "app/index.html",
            {
                "all_accounts": result[0],
                "message": result[1]
            }
        )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        result = self.__process(request)
        return render(
            request,
            "app/index.html",
            {
                "all_accounts": result[0],
                "message": result[1]
            }
        )

class RestoreView(View):
    #@csrf_exempt
    def get(self, request, *args, **kwargs):
        restoreDatabase()
        return render(request, "app/createdb.html", {})

class AddView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return render(request, "app/add.html", {"account_type": kwargs["account_type"]})

class EditView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        data = getData(kwargs["cuit"], kwargs["account_type"])
        return render(request, "app/edit.html", {"data": data})

class RemoveView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        data = getData(kwargs["cuit"], kwargs["account_type"])
        return render(request, "app/remove.html", {"data": data})

class DisplayView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        data = getData(kwargs["cuit"], kwargs["account_type"])
        return render(request, "app/view.html", {"data": data})

class CRUD(APIView):
    def get(self, request, **kwargs):
        keys = [str(key) for key in kwargs]
        data = {}

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