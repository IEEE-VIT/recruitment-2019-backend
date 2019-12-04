import json

import django_filters
import requests
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from candidate.models import Candidate
from candidate.serializers import CandidateSerializer


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

    def send_email_to_candidate(self, request, candidate_email, subject, body, sender_email, *args, **kwargs):

        try:
            mail_url = 'https://justanothersender.herokuapp.com/sendEmailsExternal'
            r = requests.post(
                url=mail_url,
                json=json.dumps(
                    {
                        "email": candidate_email,
                        "html": body,
                        "subject": subject,
                        "sender": sender_email,
                        "nameOfEmail": "IEEE-VIT Recruitments 2019",
                        "secret": "RealDevillsWithIn"
                    }
                )
            )
            if r.status_code == 200:
                print(r.content)
                return Response({'detail': "Email has been sent to candidate"}, status=200)
            else:
                print(r.content)
                return Response({'message': "Email could not been sent to candidate"}, status=400)
        except Exception as e:
            print(f"Couldn't send email to candidate. Error: {e}")
            return Response({'detail': 'Email is Invalid. We recommend deleting the candidate'}, status=400)


class CandidateListViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).order_by(
        'timestamp')
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['room_number', 'interests']
    serializer_class = CandidateSerializer
