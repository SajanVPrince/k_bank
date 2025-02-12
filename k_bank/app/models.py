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