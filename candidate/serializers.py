from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

from candidate.models import Answer, Candidate, ProjectTemplate


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer']


class CandidateSerializer(WritableNestedModelSerializer):
    answers = AnswerSerializer(many=True, source='candidate_answers')
    recaptcha = ReCaptchaField(write_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'

    def get_fields(self, *args, **kwargs):
        fields = super(CandidateSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PATCH":
            fields['id'].read_only = True
            fields['name'].read_only = True
            fields['contact'].read_only = True
            fields['reg_no'].read_only = True
            fields['email'].read_only = True
            fields['hostel'].read_only = True
            fields['interests'].read_only = True
            fields['answers'].read_only = True
            fields['timestamp'].read_only = True
            fields['called'].read_only = True
            fields['room_number'].read_only = True
            fields['times_snoozed'].read_only = True
            fields['is_active'].read_only = True

        if request and getattr(request, 'method', None) == 'POST':  # Candidate Fills This
            fields['id'].read_only = True
            fields['timestamp'].read_only = True
            fields['is_active'].read_only = True
            fields['times_snoozed'].read_only = True
            fields['called'].read_only = True
            fields['round_1_comment'].read_only = True
            fields['round_1_call'].read_only = True
            fields['round_2_project_template'].read_only = True
            fields['round_2_project_modification'].read_only = True
            fields['round_2_comment'].read_only = True
            fields['round_2_project_understanding'].read_only = True
            fields['round_2_call'].read_only = True

        return fields

    def create(self, validated_data):
        validated_data.pop('recaptcha')
        super(CandidateSerializer, self).create(validated_data=validated_data)


class ProjectTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTemplate
        fields = '__all__'
        read_only_fields = ['template_id', 'domain', 'title', 'body']


class ProjectAssignSerializer(serializers.Serializer):
    applicant_id = serializers.IntegerField(required=True)
    project_template_id = serializers.CharField(max_length=10, required=True)
    modification_body = serializers.CharField(allow_blank=True, max_length=10000)
