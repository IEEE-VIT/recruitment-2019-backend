from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets

from recruiter.models import User
from recruiter.serializers import UserSerializer


class RecruiterViewSet(viewsets.GenericViewSet, UpdateModelMixin, RetrieveModelMixin):

	queryset = User.objects.all()
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer



