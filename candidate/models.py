from django.db import models
from django.urls import reverse
from django.utils import timezone


class Candidate(models.Model):

    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    reg_no = models.CharField(max_length=9)
    email = models.EmailField()
    hostel = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    interests = models.CharField(max_length=50)
    times_snoozed = models.IntegerField(default=0)
    called = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    room_number = models.IntegerField()


    round_1_comment = models.TextField(blank=True)
    round_1_call = models.BooleanField(default=None)

    # round_2_project_template = models.ForeignKey() ToDo: Add This Foreign Key
    round_2_project_modification = models.TextField(default=None)
    round_2_comment = models.TextField(default=None)
    round_2_project_completion = models.IntegerField(default=0)
    round_2_project_understanding = models.IntegerField(default=0)
    round_2_call = models.BooleanField(default=None)



    def get_absolute_url(self):
        return reverse('candidate:candidate_detail', args=[self.reg_no])

    def save(self, *args, **kwargs):
        super(Candidate, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Answer(models.Model):
    candidate_id = models.ForeignKey('Candidate', on_delete=models.CASCADE, related_name='candidate_answers')
    answer = models.TextField()

    def __str__(self):
        return f"{self.candidate_id} - {self.answer}"
