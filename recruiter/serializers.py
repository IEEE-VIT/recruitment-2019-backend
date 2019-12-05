from rest_framework import serializers

from recruiter.models import Recruiter, User


class RecruiterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recruiter
		fields = ['id', 'is_moderator', 'is_interviewer', 'room_no']
		read_only_fields = ['id']


class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = User

		fields = '__all__'

	def create(self, validated_data):
		print('creating')
		user = super().create(**validated_data)

	def update(self, instance, validated_data):
		recruiter_data = validated_data.pop('recruiter')
		recruiter = instance.recruiter

		instance.email = validated_data.get('email', instance.email)
		instance.save()

		recruiter.is_moderator = recruiter_data.get('is_moderator', recruiter.is_moderator)
		recruiter.is_interviewer = recruiter_data.get('is_interviewer', recruiter.is_interviewer)
		recruiter.room_no = recruiter_data.get('room_no', recruiter.room_no)
		recruiter.save()

		return instance


class RegisterSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=100)
	email = serializers.EmailField()
	password = serializers.CharField(max_length=100, write_only=True)
	first_name = serializers.CharField(max_length=100)
	last_name = serializers.CharField(max_length=100)
