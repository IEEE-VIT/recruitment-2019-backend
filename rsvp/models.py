from django.db import models

# Create your models here.

class Rsvp(models.Model):
    name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=9)
    email = models.EmailField()
    contact = models.BigIntegerField()
