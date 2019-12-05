from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from rest_framework_recaptcha.fields import ReCaptchaField
from candidate.models import Answer, Candidate, ProjectTemplate


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer']


class CandidateInterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['called', 'timestamp', 'round_1_comment', 'round_1_call', 'round_2_project_template',
                  'round_2_project_modification', 'round_2_comment', 'round_2_project_completion',
                  'round_2_project_understanding', 'round_2_call']


class CandidateSerializer(WritableNestedModelSerializer):
    answers = AnswerSerializer(many=True, source='candidate_answers')
    recaptcha_field = ReCaptchaField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'contact', 'reg_no', 'email', 'hostel', 'interests', 'answers', 'timestamp', 'room_number',]
        read_only_fields = ['id', 'is_active', 'times_snoozed', 'called', 'timestamp', 'round_1_comment',
                            'round_1_call', 'round_2_project_template', 'round_2_project_modification',
                            'round_2_comment', 'round_2_project_completion', 'round_2_project_understanding',
                            'round_2_call']

    def create(self, validated_data):
        validated_data.pop('recaptcha_field')
        return super(CandidateSerializer, self).create(validated_data=validated_data)


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

