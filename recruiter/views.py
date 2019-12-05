from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from recruiter.models import User
from recruiter.serializers import RegisterSerializer


class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(methods=['post'], detail=False, url_name='register')
    @csrf_exempt
    def register(self, request):
        # Check for username exists
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            first_name = serializer.data.get('first_name')
            last_name = serializer.data.get('last_name')
        else:
            return Response({'detail': "Invalid Form Data"}, status=400)

        if username in User.objects.all().values_list('username') or email in User.objects.all().values_list('email'):
            return Response({'detail': "User with that username already exists"}, status=400)

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        return Response({'detail': "Registered Successfully, please contact Admin for Approval"}, status=201)
