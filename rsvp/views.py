# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

from .serializers import RSVPSerializer


class RsvpView(CreateAPIView):
	throttle_classes = [AnonRateThrottle]
	permission_classes = [AllowAny]
	serializer_class = RSVPSerializer


