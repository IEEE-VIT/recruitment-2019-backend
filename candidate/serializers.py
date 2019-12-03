from rest_framework import serializers

from candidate.models import Answer, Candidate

from drf_writable_nested import WritableNestedModelSerializer


class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ['id', 'answer']


class CandidateSerializer(WritableNestedModelSerializer):

	answers = AnswerSerializer(many=True, source='candidate_answers')

	class Meta:
		model = Candidate
		fields = ['url', 'id', 'name', 'contact', 'reg_no', 'email', 'hostel', 'is_active', 'interests', 'tech_interests', 'answers', 'grade', 'comment']

	def get_fields(self, *args, **kwargs):
		fields = super(CandidateSerializer, self).get_fields(*args, **kwargs)
		request = self.context.get('request', None)
		if request and getattr(request, 'method', None) == "PATCH":
			fields['name'].read_only = True
			fields['contact'].read_only = True
			fields['reg_no'].read_only = True
			fields['email'].read_only = True
			fields['hostel'].read_only = True
			fields['interests'].read_only = True
			fields['tech_interests'].read_only = True
			fields['answers'].read_only = True

		if request and getattr(request, 'method', None) == 'POST':
			fields['grade'].read_only = True
			fields['comment'].read_only = True

		return fields



