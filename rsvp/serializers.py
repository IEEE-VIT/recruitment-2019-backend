from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

from .models import RSVP


class RSVPSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaField()

    class Meta:
        model = RSVP
        exclude = ['timestamp', 'id']
