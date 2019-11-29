from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Rsvp
from .serializers import ArticleSerializer


class RsvpView(APIView):
    def post(self, request):
        rsvp = request.data.get('rsvp')

        serializer = RsvpSerializer(data=rsvp)
        if serializer.is_valid(raise_exception=True):
            rsvp_saved = serializer.save()
        return Response({"success": "Rsvp '{}' sent successfully".format(rsvp_saved.title)})

