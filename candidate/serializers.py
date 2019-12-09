from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

from candidate.models import Candidate, ProjectTemplate


class CandidateInterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['called', 'timestamp', 'round_1_comment', 'round_1_call', 'round_2_project_template',
                  'round_2_project_modification', 'round_2_comment', 'round_2_project_completion',
                  'round_2_project_understanding', 'round_2_call', 'interviewer_switch', 'interests']


class CandidateSerializer(WritableNestedModelSerializer):
    reg_no = serializers.RegexField(regex='^19[A-Z]{3}[0-9]{4}$')

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'contact', 'email', 'hostel', 'reg_no', 'interests', 'question1_text',
                  'question2_text', 'question3_text', 'room_number', 'is_active', 'times_snoozed', 'called',
                  'timestamp', 'round_1_comment', 'round_1_call', 'round_2_project_template',
                  'round_2_project_modification', 'round_2_comment', 'round_2_project_completion',
                  'round_2_project_understanding', 'round_2_call', 'called_by',
                  'interviewer_switch', 'called_to_room_no', 'answer1_text', 'answer2_text', 'answer3_text']

        read_only_fields = ['id', 'is_active', 'times_snoozed', 'called', 'timestamp', 'round_1_comment',
                            'round_1_call', 'round_2_project_template', 'round_2_project_modification',
                            'round_2_comment', 'round_2_project_completion', 'round_2_project_understanding',
                            'round_2_call', 'called_by', 'interviewer_switch', 'called_to_room_no']


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
