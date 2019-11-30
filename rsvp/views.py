# Create your views here.
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from rsvp.models import RSVP
from .serializers import RSVPSerializer


class RsvpView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RSVPSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

