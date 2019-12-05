from rest_framework import serializers

from recruiter.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
