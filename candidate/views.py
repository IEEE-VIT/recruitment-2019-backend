import django_filters
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from candidate.models import Candidate, ProjectTemplate
from candidate.serializers import CandidateSerializer, ProjectTemplateSerializer, ProjectAssignSerializer


class CandidateViewSet(viewsets.GenericViewSet, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    serializer_class = CandidateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'candidate_id'
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['room_number', 'interests']

    def get_queryset(self):
        if self.request.action == 'list':
            return Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).order_by(
                'timestamp')
        else:
            return Candidate.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'partial_update' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['POST'], detail=True)
    def snooze(self, request, *args, **kwargs):
        try:
            candidate = Candidate.objects.get(id=kwargs['candidate_id'])
        except Candidate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            # ToDo: Send Email to Candidate
            candidate.email_sent = True
            return Response({'detail': "Snooze Mail Has Been Sent"}, status=200)
        except Exception as e:
            print(f"Couldn't send email to candidate. Error: {e}")
            candidate.times_snoozed += 1
            candidate.save()
            return Response({'detail': 'Email is Invalid. We recommend deleting the candidate'})

    def invalidate(self, request, **kwargs):
        candidate = Candidate.objects.get(id=kwargs['applicant_id'])
        candidate.is_active = False
        # ToDo: Send Email to Candidate
        candidate.save()
        return Response({'detail': f"The candidate {candidate.reg_no} has been invalidated"}, status=200)


class CandidateListViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).order_by(
        'timestamp')
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['room_number', 'interests']
    serializer_class = CandidateSerializer


class ProjectTemplateViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = ProjectTemplate.objects.all()
    serializer_class = ProjectTemplateSerializer

    @action(methods=['POST'], detail=False)
    def assign(self, request):
        serializer = ProjectAssignSerializer(data=request.data)
        if serializer.is_valid():
            candidate = Candidate.objects.get(id=serializer.data['applicant_id'])
            candidate.round_2_project_template = ProjectTemplate.objects.get(
                template_id=serializer.data['project_template_id'])
            candidate.round_2_project_modification = serializer.data['modification_body']
            candidate.save()
            # ToDo: Send Email to Candidate
            return Response({'detail': "The email has been sent to the candidate"}, status=201)
        else:
            return Response({'detail': "Invalid data received"}, status=400)
