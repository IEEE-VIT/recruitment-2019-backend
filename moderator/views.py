from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from moderator.models import Moderator
from moderator.serializers import ModeratorCRUDSerializer


class ModeratorCRUDViewSet(viewsets.ModelViewSet):
    model = Moderator
    serializer_class = ModeratorCRUDSerializer
    authentication_classes = [IsAuthenticated]