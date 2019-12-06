from django.db import models


class Question(models.Model):

	question_id = models.IntegerField(primary_key=True)
	question = models.TextField()

	def __str__(self):
		return self.question
