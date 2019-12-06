# Generated by Django 2.2.7 on 2019-12-06 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_auto_20191206_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='round_1_call',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='round_2_call',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='round_2_comment',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='round_2_project_completion',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='round_2_project_template',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='candidate.ProjectTemplate'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='round_2_project_understanding',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]