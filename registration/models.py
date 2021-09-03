from django.db import models

# Create your models here.
class Registration(models.Model):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone_number= models.BigIntegerField()
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=20)