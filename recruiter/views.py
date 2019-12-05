from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from recruiter.models import User
from recruiter.serializers import UserSerializer, RegisterSerializer


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
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def register(self, request):
        # Check for username exists


        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')


        if username in User.objects.all().values_list('username') or email in User.objects.all().values_list('email'):
            return Response({'detail': "User with that username/email already exists"}, status=400)

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        return Response({'detail': "Registered Successfully, please contact Admin for Approval"}, status=201)
