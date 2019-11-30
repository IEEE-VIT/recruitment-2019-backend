from rest_framework import serializers

from moderator.models import Moderator


class ModeratorCRUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moderator
        fields = '__all__'

