from rest_framework import serializers

from .models import Rsvp


class RsvpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    reg_no = serializers.CharField(max_length=9)
    email = serializers.EmailField()
    contact = serializers.BigIntegerField()


    def create(self, validated_data):
        return Rsvp.objects.create(**validated_data)