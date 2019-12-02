from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from Recruitement_Website_Backend.permissions import IsSuperuser
from moderator.models import Moderator
from moderator.serializers import ModeratorCRUDSerializer


class ModeratorCRUDViewSet(viewsets.ModelViewSet):
    authentication_classes = [IsSuperuser]
    model = Moderator
    serializer_class = ModeratorCRUDSerializer
