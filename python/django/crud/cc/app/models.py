# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Account(models.Model):
	PHYSIC = 'F'
	LEGAL = 'J'
	
	ACCOUNT_CHOICES = [
		(PHYSIC, 'Física'),
		(LEGAL, 'Jurídica'),
	]

	cuit = models.IntegerField()
	account_type = models.CharField(max_length=1, choices=ACCOUNT_CHOICES, default=PHYSIC)

	def __str__(self):
		return "%s" % self.cuit

class Person(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
	name = models.CharField(max_length=80)
	surname = models.CharField(max_length=250)
	cardid = models.IntegerField()

	def __str__(self):
		return "%s" % self.name
	
class Company(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
	name = models.CharField(max_length=100)
	year = models.IntegerField()

	def __str__(self):
		return "%s" % self.name
