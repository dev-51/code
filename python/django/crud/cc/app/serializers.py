from rest_framework import serializers
from .models import Account, Person, Company

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('cuit', 'account_type')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('account', 'name', 'surname', 'cardid')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('account', 'name', 'year')
