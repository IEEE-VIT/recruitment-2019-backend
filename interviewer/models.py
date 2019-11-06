from django.db import models

# Create your models here.
class Interviewer (models.Model):
    name = models.CharField(max_length=20)
    room = models.CharField(max_length=6)

    def __str__(self):
        return (self.id + ' ' + self.name + ' '+ self.room)
    