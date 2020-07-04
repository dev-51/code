# -*- coding: utf-8 -*-
from .models import Account
from .database import Database

def createJSON(r):
    ob = []
    keys = []
    data = {}

    if r.method == 'POST':
        keys = [str(key) for key in r.POST.iterkeys()]
        ob = r.POST
    elif r.method == 'GET':
        keys = [str(key) for key in r.GET.iterkeys()]
        ob = r.GET

    for key in keys:
        data[key] = ob[key]

    return data

def commitInsert(params):
    db = Database(params["cuit"], params["account_type"])

    if params["account_type"] == "F":
        db.insertPerson({
            "name": params["name"],
            "surname": params["surname"],
            "cardid": params["cardid"]
        })
    elif params["account_type"] == "J":
        db.insertCompany({
            "name": params["name"],
            "year": params["year"]
        })

def commitUpdate(params):
    db = Database(params["cuit"], params["account_type"])

    if params["account_type"] == "F":
        db.updatePerson({
            "name": params["name"],
            "surname": params["surname"],
            "cardid": params["cardid"]
        })
    elif params["account_type"] == "J":
        db.updateCompany({
            "name": params["name"],
            "year": params["year"]
        })

def commitRemove(params):
    db = Database(params["cuit"], params["account_type"])

    if params["account_type"] == "F":
        db.removePerson()
    elif params["account_type"] == "J":
        db.removeCompany()

def execAction(r, rest_api = False):
    params = createJSON(r)

    if r.method == 'POST':
        keys = [str(key) for key in r.POST.iterkeys()]
    elif r.method == 'GET':
        keys = [str(key) for key in r.GET.iterkeys()]

    pre_error = None

    if "insert" in keys:
        count = Account.objects.filter(cuit=params["cuit"]).count()
        # if account exists, at least, once or more times, then operation is aborted
        if count > 0:
            pre_error = \
                "Ya existe el mismo número de cuit {}. " + \
                "Por lo tanto, no ha sido insertado a la " + \
                "base de datos."
            pre_error = pre_error.format(params["cuit"])
        else:
            commitInsert(params)
    elif "update" in keys:
        count = Account.objects.filter(cuit=params["cuit"]).count()
        # if account exists more than once, then operation is aborted
        if count > 1:
            pre_error = \
                "Atención: El número de cuit {} existe más de una vez. " + \
                "La operación de grabar en base de datos, ha sido cancelada."
            pre_error = pre_error.format(params["cuit"])
        else:
            commitUpdate(params)
    elif "remove" in keys:
        count = Account.objects.filter(cuit=params["cuit"]).count()
        # if account exists more than once, then operation is aborted
        if count > 1:
            pre_error = \
                "Atención: El número de cuit {} existe más de una vez. " + \
                "La operación de borrar en base de datos, ha sido cancelada."
            pre_error = pre_error.format(params["cuit"])
        else:
            commitRemove(params)

    if rest_api:
        if pre_error:
            pre_error = pre_error.decode("utf8")

    return pre_error
