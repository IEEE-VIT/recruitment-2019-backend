from django.db import models


class Question(models.Model):

	APTITUDE = 'AT'
	SWOT = 'ST'

	type_choices = [
		(APTITUDE, 'Aptitude'),
		(SWOT, 'Swot')
	]

	question_id = models.IntegerField(primary_key=True)
	question = models.TextField()
	type = models.CharField(choices=type_choices, max_length=5)

	def __str__(self):
		return self.question