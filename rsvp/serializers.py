from recaptcha.fields import ReCaptchaField
from rest_framework import serializers

from .models import RSVP


class RSVPSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaField(write_only=True)

    class Meta:
        model = RSVP
        exclude = ['timestamp', 'id']
