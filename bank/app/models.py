from django.db import models
from django.contrib.auth.models import *
# Create your models here.

class Openacc(models.Model):
    accountnumber = models.IntegerField()
    email = models.EmailField()
    fullname = models.TextField()
    phone = models.TextField()
    address = models.TextField()

class Approved(models.Model):
    account=models.ForeignKey(Openacc,on_delete=models.CASCADE)

class Bank(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    accountnumber = models.IntegerField()
    balance = models.IntegerField()
    email = models.EmailField()
    fullname = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    photo = models.FileField()
    proof = models.FileField()


class Availible(models.Model):
    accountnumber = models.IntegerField()


class Updates(models.Model):
    title=models.TextField()
    discription=models.TextField()