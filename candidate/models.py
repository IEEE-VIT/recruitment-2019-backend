from django.db import models


class Candidate(models.Model):
	name = models.CharField(max_length=100)
	contact = models.BigIntegerField()
	reg_no = models.CharField(max_length=9)
	email = models.EmailField()
	hostel = models.CharField(max_length=10)
	grade = models.CharField(max_length=10, blank=True)
	comment = models.TextField(blank=True)

	def save(self, *args, **kwargs):
		super(Candidate, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Answer(models.Model):
	candidate_id = models.ForeignKey('Candidate', on_delete=models.CASCADE, related_name='candidate_answers')
	answer = models.TextField()

	def __str__(self):
		return f"{self.candidate_id} - {self.answer}"