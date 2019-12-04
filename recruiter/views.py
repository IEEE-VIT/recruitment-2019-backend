from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from recruiter.models import User, create_auth_token
from recruiter.serializers import UserSerializer


class RecruiterViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):

	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		if self.action == 'create':
			permission_classes = [AllowAny]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]


class AuthViewSet(ViewSet):

	@action(methods=['post'], detail=False, url_name='registration')
	@csrf_exempt
	def register(self, request):
		# Check for username exists
		username = request.data.get('username')
		email = request.data.get('email')
		password = request.data.get('password')
		first_name = request.data.get('first_name')
		last_name = request.data.get('last_name')

		if username in User.objects.all().values_list('username'):
			return Response({'detail': "User with that username already exists"}, status=400)

		user = User()
		user.username = username
		user.email = email
		user.set_password(password)
		user.first_name = first_name
		user.last_name = last_name
		user.is_active = False
		user.save()
		return Response(status=201)

