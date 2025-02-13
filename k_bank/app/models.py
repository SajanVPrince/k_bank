from django.db import models

# Create your models here.

class Openacc(models.Model):
    accountnumber = models.IntegerField()
    email = models.EmailField()
    fullname = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    photo = models.FileField()
    proof = models.FileField()

class Approved(models.Model):
    account=models.ForeignKey(Openacc,on_delete=models.CASCADE)

class Bank(models.Model):
    accountnumber = models.IntegerField()

class Register(models.Model):
    accountnumber = models.ForeignKey(Bank,on_delete=models.CASCADE)
    email = models.EmailField()
    fullname = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    photo = models.FileField()
    proof = models.FileField()

class Balance(models.Model):
    accountnumber = models.ForeignKey(Bank,on_delete=models.CASCADE)
    balance = models.IntegerField()