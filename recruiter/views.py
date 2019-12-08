from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, permission_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from recruiter.models import User, AvailableRoom
from recruiter.permissions import IsLoggedInUserOrAdmin
from recruiter.serializers import RegisterSerializer, UserSerializer, AvailableRoomSerializer


class UserViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    permission_classes = [IsLoggedInUserOrAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def get_logged_in_user(self, request):
        logged_in_user = self.request.user
        return Response({'user_id': logged_in_user.id}, status=200)


class AuthViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(methods=['post'], detail=False, url_name='register', permission_classes=[AllowAny])
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

    @action(methods=['post'], detail=False, url_name='logout', permission_classes=[IsLoggedInUserOrAdmin])
    @csrf_exempt
    def logout(self, request, **kwargs):
        print(request.user.auth_token)
        request.user.auth_token.delete()
        return Response({'detail': "Successfully logged out"}, status=200)


class AvailableRoomViewset(ModelViewSet):

    queryset = AvailableRoom.objects.all()
    serializer_class = AvailableRoomSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super(AvailableRoomViewset, self).get_permissions()