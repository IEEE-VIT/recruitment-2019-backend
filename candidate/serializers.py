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
		fields = ['id', 'name', 'contact', 'reg_no', 'email', 'hostel', 'grade', 'comment', 'answers']

