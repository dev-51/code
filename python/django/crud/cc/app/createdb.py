from .models import Account, Person, Company

def restoreDatabase():
    # --------------------------
    # Elimino a todos los Titulares
    # --------------------------
    Account.objects.all().delete()

    # --------------------------
    # Titulares Fisicos
    # --------------------------
    account=Account(cuit=30710647011, account_type="F")
    account.save()
    person = Person(account=account, name="Roberto", surname="Ruiz", cardid=27066345)
    person.save()

    account=Account(cuit=31610996184, account_type="F")
    account.save()
    person = Person(account=account, name="Cesar", surname="Garcia", cardid=25067345)
    person.save()

    account=Account(cuit=32615506183, account_type="F")
    account.save()
    person = Person(account=account, name="Maria", surname="Selena", cardid=25066305)
    person.save()

    # --------------------------
    # Titulares Juridicos
    # --------------------------
    account=Account(cuit=30117706184, account_type="J")
    account.save()
    company = Company(account=account, name="Robotics", year=1994)
    company.save()

    account=Account(cuit=30917706187, account_type="J")
    account.save()
    company = Company(account=account, name="Kiosco 24HS", year=1992)
    company.save()

    account=Account(cuit=30618806189, account_type="J")
    account.save()
    company = Company(account=account, name="Dietetica Rosa", year=2003)
    company.save()
