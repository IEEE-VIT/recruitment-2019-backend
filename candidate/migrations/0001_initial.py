# Generated by Django 2.2.7 on 2019-12-06 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTemplate',
            fields=[
                ('template_id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('domain', models.CharField(max_length=20)),
                ('title', models.TextField()),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact', models.BigIntegerField(unique=True)),
                ('reg_no', models.CharField(max_length=9, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('hostel', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('interests', models.CharField(max_length=50)),
                ('times_snoozed', models.IntegerField(default=0)),
                ('called', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('room_number', models.CharField(max_length=10)),
                ('interviewer_switch', models.BooleanField(blank=True, default=False, null=True)),
                ('question1_text', models.TextField(blank=True, null=True)),
                ('question2_text', models.TextField(blank=True, null=True)),
                ('question3_text', models.TextField(blank=True, null=True)),
                ('round_1_comment', models.TextField(blank=True)),
                ('round_1_call', models.BooleanField(blank=True, default=None, null=True)),
                ('round_2_project_modification', models.TextField(blank=True, default=None, null=True)),
                ('round_2_comment', models.TextField(blank=True, default=None, null=True)),
                ('round_2_project_completion', models.IntegerField(blank=True, default=0, null=True)),
                ('round_2_project_understanding', models.IntegerField(blank=True, default=0, null=True)),
                ('round_2_call', models.BooleanField(blank=True, default=False, null=True)),
                ('called_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='interviewee', to=settings.AUTH_USER_MODEL)),
                ('question1_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='candidate_question_1', to='questions.Question')),
                ('question2_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='candidate_question_2', to='questions.Question')),
                ('question3_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='candidate_question_3', to='questions.Question')),
                ('round_2_project_template', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='candidate.ProjectTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_answers', to='candidate.Candidate')),
            ],
        ),
    ]
