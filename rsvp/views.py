# Create your views here.
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import RSVPSerializer


class RsvpView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RSVPSerializer


