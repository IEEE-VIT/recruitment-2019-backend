from rest_framework import serializers

from recruiter.models import Recruiter, User

class RecruiterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recruiter
		fields = ['id', 'is_moderator', 'is_interviewer', 'room_no']


class UserSerializer(serializers.HyperlinkedModelSerializer):
	recruiter = RecruiterSerializer(required=True)

	class Meta:
		model = User

		fields = ['url', 'id', 'email', 'first_name', 'last_name', 'username', 'password', 'recruiter']
		extra_kwargs = {'password': {'write_only': True}}


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
