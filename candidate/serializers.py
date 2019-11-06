from rest_framework import serializers

from candidate.models import Answer, Candidate


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Answer
		fields = ['url', 'id', 'answer']


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
	 
	answers = AnswerSerializer(many=True, required=False)

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



