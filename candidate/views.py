from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from Recruitement_Website_Backend.functions import send_email_to_candidate
from candidate.models import Candidate, ProjectTemplate
from candidate.serializers import CandidateSerializer, ProjectTemplateSerializer, ProjectAssignSerializer, \
    AcceptRejectSerializer, CandidateInterviewerSerializer

subject = 'IEEE-VIT Recruitments 2019 Round 1'
message = f'Hi! Please report'


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Endpoint to Enable Creation Of New Candidates. To Be Used For The Round 1 Form. Many of these fields are read only, but do not appear so in the description below."
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="This Endpoint Is To Be Used By The Interviewer To Add Comments and Ratings. Many of these fields are read only, but do not appear so in the description below."
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="This Endpoint Is To Be Used By The Interviewer To Add Comments and Ratings. Many of these fields are read only, but do not appear so in the description below."
))
@method_decorator(name='snooze', decorator=swagger_auto_schema(
    operation_description="This Endpoint Is To Be Used To Snooze A Called Candidate. To Be Used By The Moderator"
))
@method_decorator(name='invalidate', decorator=swagger_auto_schema(
    operation_description="After Snoozing Multiple Times, The Candidate May Be Made Inactive. This Endpoint Allows The Moderators To Do That"
))
@method_decorator(name='accept', decorator=swagger_auto_schema(
    operation_description="This Endpoint Accepts The Candidate To The Next Round.",
))
@method_decorator(name='reject', decorator=swagger_auto_schema(
    operation_description="This Endpoint Rejects The Candidate and Also Deactivates It.",
))
class CandidateViewSet(viewsets.GenericViewSet, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    throttle_classes = [AnonRateThrottle]
    lookup_field = 'id'
    lookup_url_kwarg = 'candidate_id'
    queryset = Candidate.objects.all()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CandidateViewSet, self).dispatch(*args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(CandidateViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'retrieve':
            return CandidateSerializer
        else:
            return CandidateInterviewerSerializer

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     super().create(request)

    @action(methods=['POST'], detail=True)
    def snooze(self, request, *args, **kwargs):
        try:
            candidate = self.get_object()
        except Candidate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            send_email_to_candidate(self, candidate_email='ith.ieeevit@gmail.com',
                                    subject=subject, body=message,
                                    sender_email='jaiswalsanskar078@gmail.com')
            candidate.email_sent = True
            return Response({'detail': "Snooze Mail Has Been Sent"}, status=200)
        except Exception as e:
            print(f"Couldn't send email to candidate. Error: {e}")
            candidate.times_snoozed += 1
            candidate.save()
            return Response({'detail': 'Email is Invalid. We recommend deleting the candidate'})

    @action(methods=['POST'], detail=True)
    def invalidate(self, request, **kwargs):
        candidate = self.get_object()
        candidate.is_active = False
        send_email_to_candidate(candidate_email='sanskar.jaiswal2018@vitstudent.ac.in', subject=subject,
                                message=message, sender_email='jaiswalsanskar078@gmail.com')
        candidate.save()
        return Response({'detail': f"The candidate {candidate.reg_no} has been invalidated"}, status=200)

    @action(methods=['POST'], detail=True, serializer_class=AcceptRejectSerializer)
    def accept(self, request, **kwargs):
        candidate = self.get_object()
        round_no = request.data.get('round')
        if round_no == 1:
            candidate.round_1_call = True
            candidate.save()
            return Response({'detail': "Round 1 Rejected"}, status=200)
        elif round_no == 2:
            candidate.round_2_call = True
            candidate.save()
            return Response({'detail': "Round 2 Rejected"}, status=200)
        else:
            return Response({'detail': "Invalid Form Data"}, status=400)

    @action(methods=['POST'], detail=True, serializer_class=AcceptRejectSerializer)
    def reject(self, request, **kwargs):
        candidate = self.get_object()
        candidate.is_active = False
        round_no = request.data.get('round')
        if round_no == 1:
            candidate.round_1_call = False
            candidate.save()
            return Response({'detail': "Round 1 Passed"}, status=200)
        elif round_no == 2:
            candidate.round_2_call = False
            candidate.save()
            return Response({'detail': "Round 2 Passed"}, status=200)
        else:
            return Response({'detail': "Invalid Form Data"}, status=400)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Return A List Of Candidates Filtered According To Parameters Passed"
))
class CandidateListViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).order_by(
        'timestamp')
    serializer_class = CandidateSerializer
    throttle_classes = [AnonRateThrottle]
    filter_backends = []

    def get_queryset(self):
        candidate_interest = self.request.query_params.get('interest', None)
        room_no = self.request.query_params.get('room_no', None)
        print(type(candidate_interest))
        if self.request.method == 'GET' and candidate_interest is not None:
            return Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).filter(
                interests__contains=candidate_interest).order_by(
                'timestamp')
        elif self.request.method == 'GET' and room_no is not None:
            return Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).filter(room_number=room_no).order_by(
                'timestamp')
        else:
            return Candidate.objects.all()


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Return A List Of All The Project Templates"
))
@method_decorator(name='assign', decorator=swagger_auto_schema(
    operation_description="Endpoint To Assign Projects To Candidates and Also Any Modifications That May Be Mentioned."
))
class ProjectTemplateViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = ProjectTemplate.objects.all()
    serializer_class = ProjectTemplateSerializer

    @action(methods=['POST'], detail=False)
    def assign(self, request):
        serializer = ProjectAssignSerializer(data=request.data)
        if serializer.is_valid():
            candidate = Candidate.objects.get(id=serializer.data['applicant_id'])
            send_email_to_candidate(candidate_email='sanskar.jaiswal2018@vitstudent.ac.in', subject=subject,
                                    message=message, sender_email='jaiswalsanskar078@gmail.com')
            candidate.round_2_project_template = ProjectTemplate.objects.get(
                template_id=serializer.data['project_template_id'])
            candidate.round_2_project_modification = serializer.data['modification_body']
            candidate.save()
            return Response({'detail': "The email has been sent to the candidate"}, status=201)
        else:
            return Response({'detail': "Invalid data received"}, status=400)
