from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RSVP
from .serializers import RSVPSerializer


class RsvpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RSVPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "RSVP Received"}, status=201)
        else:
            return Response({'Failure': "Form Validation Failed"}, status=400)

