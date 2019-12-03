from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

from .models import RSVP


class RSVPSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaField()

    class Meta:
        model = RSVP
        exclude = ['timestamp', 'id']

    def create(self, validated_data):
        rsvp = RSVP.objects.create(name=validated_data['name'], contact=validated_data['contact'], reg_no=validated_data['reg_no'], email=validated_data['email'])
        return rsvp

