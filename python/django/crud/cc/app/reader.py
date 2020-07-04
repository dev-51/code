# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .models import Account, Person, Company
from .serializers import PersonSerializer, CompanySerializer

def getRows():
    all_accounts = Account.objects.all()
    len_accounts = Account.objects.count()
    list = []

    if len_accounts:
        for account in all_accounts:
            if account.account_type == "F":
                try:
                    person = Person.objects.get(account=account)
                except ObjectDoesNotExist:
                    person = None

                if person:
                    list.append({
                        "cuit": account.cuit,
                        "cuit_label": str(account.cuit)[:2] + "-" + str(account.cuit)[2:10] + "-" + str(account.cuit)[-1:],
                        "name": person.name + " " + person.surname,
                        "account_type": account.account_type
                    })
            elif account.account_type == "J":
                try:
                    company = Company.objects.get(account=account)
                except ObjectDoesNotExist:
                    company = None

                if company:
                    list.append({
                        "cuit": account.cuit,
                        "cuit_label": str(account.cuit)[:2] + "-" + str(account.cuit)[2:10] + "-" + str(account.cuit)[-1:],
                        "name": company.name,
                        "account_type": account.account_type
                    })

    return list

def getData(cuit, account_type, rest_api = False):
    data = {}
    account = None

    try:
        account = Account.objects.get(cuit=cuit)
    except (MultipleObjectsReturned) as e:
        data = {
            "error":
                "Lo siento, pero existe más de un registro " + \
                "con el mismo número de cuit {}."
        }
        data["error"] = data["error"].format(cuit)

        if rest_api:
            data["error"] = data["error"].decode("utf8")

    if account:
        if account_type == "F":
            if rest_api:
                person = PersonSerializer(Person.objects.get(account=account)).data
            else:
                person = Person.objects.get(account=account)

            data = {
                "error": None,
                "person": person,
                "account_type": account_type
            }
        elif account_type == "J":
            if rest_api:
                company = CompanySerializer(Company.objects.get(account=account)).data
            else:
                company = Company.objects.get(account=account)

            data = {
                "error": None,
                "company": company,
                "account_type": account_type
            }

    return data
