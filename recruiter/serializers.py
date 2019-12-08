from rest_framework import serializers

from recruiter.models import User, AvailableRoom


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)


class AvailableRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableRoom
        fields = ['room_number']