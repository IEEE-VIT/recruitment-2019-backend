from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

from candidate.models import Answer, Candidate, ProjectTemplate


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer']


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['called', 'timestamp', 'round_1_comment', 'round_1_call', 'round_2_project_template',
                  'round_2_project_modification', 'round_2_comment', 'round_2_project_completion',
                  'round_2_project_understanding', 'round_2_call']


class CandidateSerializer(serializers.ModelSerializer):
    answers_provided = AnswerSerializer(many=True)
    # recaptcha = ReCaptchaField(write_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ['id', 'is_active', 'times_snoozed', 'called', 'timestamp', 'round_1_comment',
                            'round_1_call', 'round_2_project_template', 'round_2_project_modification',
                            'round_2_comment', 'round_2_project_completion', 'round_2_project_understanding',
                            'round_2_call']

    def create(self, validated_data):
        # validated_data.pop('recaptcha')
        print("Create Method Reached")
        answers = validated_data.pop('answers_provided')
        print("Answers Popped")
        candidate = Candidate.objects.create(**validated_data)
        print("Candidate Created")
        for answer in answers:
            Answer.objects.create(candidate_id=candidate, **answer)
        return candidate


class ProjectTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTemplate
        fields = '__all__'
        read_only_fields = ['template_id', 'domain', 'title', 'body']


class ProjectAssignSerializer(serializers.Serializer):
    applicant_id = serializers.IntegerField(required=True)
    project_template_id = serializers.CharField(max_length=10, required=True)
    modification_body = serializers.CharField(allow_blank=True, max_length=10000)


class AcceptRejectSerializer(serializers.Serializer):
    round = serializers.IntegerField(required=True)
