# Generated by Django 2.2.7 on 2019-12-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_auto_20191207_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='answer1_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='answer2_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='answer3_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]