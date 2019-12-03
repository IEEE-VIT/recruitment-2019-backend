from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets

from recruiter.models import User
from recruiter.serializers import UserSerializer


class RecruiterViewSet(viewsets.GenericViewSet, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin):

	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		if self.action == 'create':
			permission_classes = [AllowAny]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]