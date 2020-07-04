from .models import Account, Person, Company

class Database:
    def __init__(self, cuit, account_type):
        self.cuit = cuit
        self.account_type = account_type

    def insertPerson(self, record):
        account = Account(cuit=self.cuit, account_type=self.account_type)
        account.save()

        person = Person(
            account=account,
            name=record["name"],
            surname=record["surname"],
            cardid=record["cardid"]
        )
        person.save()

    def updatePerson(self, record):
        account = Account.objects.get(cuit=self.cuit)
        person = Person.objects.get(account=account)

        person.name = record["name"]
        person.surname = record["surname"]
        person.cardid = record["cardid"]
        person.save()

    def removePerson(self):
        account = Account.objects.get(cuit=self.cuit)
        account.delete()

    def insertCompany(self, record):
        account = Account(cuit=self.cuit, account_type=self.account_type)
        account.save()

        company = Company(
            account=account,
            name=record["name"],
            year=record["year"]
        )
        company.save()

    def updateCompany(self, record):
        account = Account.objects.get(cuit=self.cuit)
        company = Company.objects.get(account=account)

        company.name = record["name"]
        company.year = record["year"]
        company.save()

    def removeCompany(self):
        account = Account.objects.get(cuit=self.cuit)
        account.delete()
