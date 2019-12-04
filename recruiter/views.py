from django.contrib.auth import authenticate
from django.contrib.sites import requests

from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response

from recruiter.models import User, create_auth_token
from recruiter.serializers import UserSerializer


class RecruiterViewSet(viewsets.GenericViewSet, UpdateModelMixin, RetrieveModelMixin):

	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		if self.action == 'create':
			permission_classes = [AllowAny]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]


class AuthViewSet():

	@action(methods=['post'], detail=False, url_name='Register')
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
		Response.status_code = 201
		return Response()

	@action(methods=['post'], detail=False)
	def login(self, request):
		"""
		Allows user to log in

		"""
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		print("User authenticated")

		if user is not None:
			print("User exists")
			if user.is_active:
				print("User is active")
				token = create_auth_token()
				Response.status_code = 200
				return Response({'token': token})
			else:
				Response.status_code = 400
				return Response({'message': 'Account not activated'})
		else:
			Response.status_code = 401
			return Response({'message': 'Password or Username incorrect'})
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer



