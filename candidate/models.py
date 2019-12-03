from django.db import models
from django.urls import reverse
from django.utils import timezone


class Candidate(models.Model):

    Management = 'Man'
    Technical = 'Tech'
    Design = 'Des'
    Filmmaking = 'Film'

    Machine_Learning = 'ML'
    Frontend = 'FE'
    Backend = 'BE'
    Electronics = 'EL'
    Cybersec = 'CS'
    Competitve_Coding = 'CC'

    INTERESTS_CHOICES =[
        (Management, 'Management'),
        (Technical, 'Technical'),
        (Design, 'Design'),
        (Filmmaking, 'Filmmaking')
    ]

    TECH_INTEREST_CHOICES = [
        (Machine_Learning, 'Machine Learning'),
        (Frontend, 'Frontend'),
        (Backend, 'Backend'),
        (Electronics, 'Electronics'),
        (Cybersec, 'Cybersec'),
        (Competitve_Coding, 'Competitive Coding')
    ]

    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    reg_no = models.CharField(max_length=9)
    email = models.EmailField()
    hostel = models.CharField(max_length=10)
    grade = models.CharField(max_length=10, blank=True)
    comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    interests = models.CharField(max_length=5, choices=INTERESTS_CHOICES)
    tech_interests = models.CharField(max_length=2, choices=TECH_INTEREST_CHOICES)
    times_snoozed = models.IntegerField(default=0)
    called = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    room_number = models.IntegerField()
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
