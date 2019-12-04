import django_filters
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from candidate.models import Candidate
from candidate.serializers import CandidateSerializer


class CandidateViewSet(viewsets.GenericViewSet, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'candidate_id'

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

        if request.method == 'PATCH':
            try:
                subject = 'IEEE-VIT 2019 Recruitments'
                message = f"Hi, {candidate.name}! Please report to {request.user.recruiter_set.all()}"
                print(message)
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='jaiswalsanskar078@gmail.com',
                    recipient_list=[candidate.email]
                )
                candidate.times_snoozed = candidate.times_snoozed+1
            except:
                print('Couldn\'t send email to candidate')


class CandidateListViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).order_by('timestamp')
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['room_number', 'interests']
    serializer_class = CandidateSerializer

