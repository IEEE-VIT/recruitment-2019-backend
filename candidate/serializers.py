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
		fields = ['url', 'id', 'name', 'contact', 'reg_no', 'email', 'hostel', 'grade', 'comment', 'answers']

	def create(self, validated_data):
		print(validated_data)
		if 'answers' in validated_data.keys():
			answers_data = validated_data.pop('answers')
			candidate = Candidate.objects.create(**validated_data)
			for answer_data in answers_data:
				Answer.objects.create(candidate_id=candidate, **answer_data)
			return candidate
		else:
			return Candidate(**validated_data)



