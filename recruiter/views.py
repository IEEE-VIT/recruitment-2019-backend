from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from recruiter.models import User
from recruiter.permissions import IsAdminUser
from recruiter.serializers import UserSerializer


class RecruiterViewSet(ModelViewSet):

	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		permission_classes = []
		if self.action == 'create':
			permission_classes = [AllowAny]
		elif self.action == 'partial_update':
			permission_classes = [IsAuthenticated]
		else:
			permission_classes = [IsAdminUser]
		return [permission() for permission in permission_classes]