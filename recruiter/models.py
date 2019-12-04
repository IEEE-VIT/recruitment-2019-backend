from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
	username = models.CharField(max_length=50)
	email = models.EmailField(unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	def __str__(self):
		return "{}".format(self.email)


class Recruiter(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter')
	is_interviewer = models.BooleanField(default=False)
	is_moderator = models.BooleanField(default=False)
	room_no = models.CharField(max_length=10)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		token = Token.objects.create(user=instance)
		return token.key
