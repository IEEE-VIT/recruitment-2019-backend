import django_filters
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from Recruitement_Website_Backend.functions import send_email_to_candidate
from candidate.models import Candidate, ProjectTemplate
from candidate.serializers import CandidateSerializer, ProjectTemplateSerializer, ProjectAssignSerializer, \
	AcceptRejectSerializer, CandidateInterviewerSerializer

round_number = 1
if round_number == 1:
	round_status = None
else:
	round_status = True


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
			self.permission_classes = [AllowAny, ]
		else:
			self.permission_classes = [IsAuthenticated, ]

		return super(CandidateViewSet, self).get_permissions()

	def get_serializer_class(self):
		if self.action == 'create' or self.action == 'retrieve':
			return CandidateSerializer
		elif self.action == 'update' or self.action == 'partial_update':
			return CandidateInterviewerSerializer
		elif self.action == 'snooze' or self.action == 'invalidate':
			return None
		elif self.action == 'accept' or self.action == 'reject':
			return AcceptRejectSerializer
		else:
			return None

	@action(methods=['POST'], detail=True)
	def snooze(self, request, *args, **kwargs):
		try:
			candidate = self.get_object()
		except Candidate.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		subject = "IEEE - VIT | Recruitment Notification"
		body = f"Dear {candidate.name},<br>We attempted to call you for your interview but it seems like you didn't turn up. Please report to the room that you filled your form in and talk to the moderator<br><br>Warm Regards,<br>Team IEEE - VIT"

		try:
			send_email_to_candidate(candidate_email=candidate.email,
			                        subject=subject, mail_body=body)
			candidate.times_snoozed += 1
			candidate.save()
			return Response({'detail': "Snooze Mail Has Been Sent"}, status=200)
		except Exception as e:
			print(f"Couldn't send email to candidate. Error: {e}")

			return Response({'detail': 'Email is Invalid. We recommend deleting the candidate'})

	@action(methods=['POST'], detail=True)
	def invalidate(self, request, **kwargs):
		candidate = self.get_object()
		candidate.is_active = False

		subject = "IEEE - VIT | Recruitment Notification"
		body = f"Dear {candidate.name},<br>We attempted to call you for your interview but were unable to reach you. We also sent you notification, but you were not available which is why we had to invalidate your entry. Please report to any of the moderators in case you are still interested. <br><br>Warm Regards,<br>Team IEEE - VIT"

		send_email_to_candidate(candidate_email=candidate.email, subject=subject,
		                        mail_body=body)
		candidate.save()
		return Response({'detail': f"The candidate {candidate.reg_no} has been invalidated"}, status=200)

	@action(methods=['POST'], detail=True, serializer_class=AcceptRejectSerializer)
	def accept(self, request, **kwargs):
		candidate = self.get_object()
		round_no = request.data.get('round')
		candidate.interviewer_switch = False
		if round_no == 1:
			candidate.round_1_call = True
			candidate.called = False
			candidate.save()
			return Response({'detail': "Round 1 Passed"}, status=200)
		elif round_no == 2:
			candidate.round_2_call = True
			candidate.called = False
			candidate.save()
			return Response({'detail': "Round 2 Passed"}, status=200)
		else:
			return Response({'detail': "Invalid Form Data"}, status=400)

	@action(methods=['POST'], detail=True, serializer_class=AcceptRejectSerializer)
	def reject(self, request, **kwargs):
		#Reject endpoint
		candidate = self.get_object()
		candidate.is_active = False
		candidate.interviewer_switch = False
		candidate.called = False
		round_no = request.data.get('round')
		print(type(round_no))
		if round_no == 1:
			candidate.round_1_call = False
			candidate.save()
			return Response({'detail': "Round 1 Rejected"}, status=200)
		elif round_no == 2:
			candidate.round_2_call = False
			candidate.save()
			return Response({'detail': "Round 2 Rejected"}, status=200)
		else:
			return Response({'detail': "Invalid Form Data"}, status=400)

	@action(methods=['POST'], detail=True)
	def call(self, request, **kwargs):
		candidate = self.get_object()
		if candidate.called:
			return Response(
				{'detail': 'This candidate has already been called. Please contact admin if you want to call again'},
				status=400)
		candidate.called = True
		interviewer = request.user
		candidate.called_by = interviewer.username
		candidate.called_to_room_no = interviewer.room_no
		print(candidate.called)
		mail_subject = "IEEE - VIT Recruitment Interview Alert"
		mail_body = f"Dear {candidate.name},<br>We thank you for your patience. You have been called for your interview. Please " \
			f"inform the moderator in your room and make your way to room number {interviewer.room_no}. Your " \
			f"interview will be conducted by {interviewer.first_name} {interviewer.last_name}.<br><br>Warm " \
			f"Regards,<br>Team IEEE - VIT. "
		mail_to = candidate.email

		# send_email_to_candidate(mail_to, mail_subject, mail_body)
		candidate.save()
		return Response({'detail': 'Candidate called!'}, status=200)

	@action(methods=['POST'], detail=True)
	def send_to_another_interviewer(self, request, **kwargs):
		candidate = self.get_object()
		candidate.interviewer_switch = True
		candidate.save()
		return Response({'detail': 'Interviewer successfully changed!'}, status=200)


@method_decorator(name='list', decorator=swagger_auto_schema(
	operation_description="Return A List Of Candidates Filtered According To Parameters Passed"
))
class CandidateListViewSet(viewsets.GenericViewSet, ListModelMixin):
	# queryset = Candidate.objects.filter(Q(called=False) & (Q(round_1_call=None) | Q(round_2_call=None))).order_by(
	# 	'timestamp')
	throttle_classes = [AnonRateThrottle]
	serializer_class = CandidateSerializer
	filter_backends = []

	def get_queryset(self):
		candidate_interest = self.request.query_params.get('interest', None)
		room_no = self.request.query_params.get('room_no', None)
		print(type(room_no))
		print(room_no)
		if self.request.method == 'GET' and candidate_interest is not None:  # for Interviewer
			return Candidate.objects.filter(
				Q(called=False) & Q(is_active=True) & Q(round_1_call=False) & Q(round_2_call=False) & Q(interviewer_switch=False)).filter(
				interests__contains=candidate_interest).order_by('timestamp')

		elif self.request.method == 'GET' and room_no is not None:  # for Moderator
			return Candidate.objects.filter(
				Q(called=True) & Q(is_active=True) & Q(round_1_call=False) & Q(round_2_call=False) & Q(interviewer_switch=False)).filter(
				room_number__exact=room_no).order_by(
				'timestamp')

	@action(methods=['GET'], detail=False, serializer_class=CandidateInterviewerSerializer,
	        permission_classes=[IsAuthenticated])
	def interviewer_switched_candidates(self, *args, **kwargs):
		candidates = Candidate.objects.filter(interviewer_switch=True)
		print(candidates)
		return Response({'interviewer_switched_candidates': candidates.values()}, status=200)


@method_decorator(name='list', decorator=swagger_auto_schema(
	operation_description="Return A List Of All The Project Templates"
))
@method_decorator(name='assign', decorator=swagger_auto_schema(
	operation_description="Endpoint To Assign Projects To Candidates and Also Any Modifications That May Be Mentioned."
))
class ProjectTemplateViewSet(viewsets.GenericViewSet, ListModelMixin):
	queryset = ProjectTemplate.objects.all()
	serializer_class = ProjectTemplateSerializer
	filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
	filterset_fields = ['domain']

	@action(methods=['POST'], detail=False)
	def assign(self, request):
		serializer = ProjectAssignSerializer(data=request.data)
		if serializer.is_valid():
			candidate = Candidate.objects.get(id=serializer.data['applicant_id'])
			candidate.round_2_project_template = ProjectTemplate.objects.get(
				template_id=serializer.data['project_template_id'])
			candidate.round_2_project_modification = serializer.data['modification_body']
			candidate.save()
			subject = "IEEE - VIT | Round 2 Project"
			body = f"Dear Applicant,<br>Congratulations on clearing the first round of interviews. You have been assigned the following project:<br><code>{candidate.round_2_project_template.body}<br>A few more instructions:<br>{candidate.round_2_project_modification}</code><br>Do your very best!<br>Warm Regards,<br>Team IEEE - VIT"
			send_email_to_candidate(candidate_email=candidate.email, subject=subject, mail_body=body)
			return Response({'detail': "The email has been sent to the candidate"}, status=200)
		else:
			return Response({'detail': "Invalid data received"}, status=400)
