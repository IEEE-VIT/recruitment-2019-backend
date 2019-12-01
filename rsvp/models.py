from django.db import models

# Create your models here.
from django.utils import timezone


class RSVP(models.Model):
    name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    contact = models.BigIntegerField(unique=True)
    timestamp = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.name
