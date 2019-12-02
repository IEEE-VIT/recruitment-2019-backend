from rest_framework.viewsets import ModelViewSet

from Recruitement_Website_Backend.permissions import IsSuperuser
from candidate.models import Candidate
from candidate.serializers import CandidateSerializer


class CandidateViewSet(ModelViewSet):
	permission_classes = [IsSuperuser]
	serializer_class = CandidateSerializer
	queryset = Candidate.objects.all()
