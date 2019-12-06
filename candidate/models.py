from django.db import models
from django.urls import reverse
from django.utils import timezone

from recruiter.models import User


class ProjectTemplate(models.Model):
    template_id = models.CharField(max_length=4, primary_key=True)
    domain = models.CharField(max_length=20)
    title = models.TextField()
    body = models.TextField()


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    contact = models.BigIntegerField(unique=True)
    reg_no = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    hostel = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    interests = models.CharField(max_length=50)
    times_snoozed = models.IntegerField(default=0)
    called = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    room_number = models.CharField(max_length=10)
    interviewer_switch = models.BooleanField(default=False, null=True, blank=True)
    
    question1_id = models.ForeignKey('questions.Question', null=True, blank=True, on_delete=models.PROTECT, related_name='candidate_question_1')
    question2_id = models.ForeignKey('questions.Question', null=True, blank=True, on_delete=models.PROTECT, related_name='candidate_question_2')
    question3_id = models.ForeignKey('questions.Question', null=True, blank=True, on_delete=models.PROTECT, related_name='candidate_question_3')

    question1_text = models.TextField(null=True, blank=True)
    question2_text = models.TextField(null=True, blank=True)
    question3_text = models.TextField(null=True, blank=True)
    
    round_1_comment = models.TextField(blank=True)
    round_1_call = models.BooleanField(default=None, null=True, blank=True)

    round_2_project_template = models.ForeignKey(ProjectTemplate, on_delete=models.PROTECT, default=None, null=True, blank=True)
    round_2_project_modification = models.TextField(default=None, blank=True, null=True)
    round_2_comment = models.TextField(default=None, null=True, blank=True)
    round_2_project_completion = models.IntegerField(default=0, null=True, blank=True)
    round_2_project_understanding = models.IntegerField(default=0, null=True, blank=True)
    round_2_call = models.BooleanField(default=False, null=True, blank=True)

    called_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="interviewee", null=True, blank=True)

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

