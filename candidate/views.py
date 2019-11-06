from rest_framework.viewsets import ModelViewSet

from candidate.models import Candidate
from candidate.serializers import CandidateSerializer


class CandidateViewSet(ModelViewSet):
	serializer_class = CandidateSerializer
	queryset = Candidate.objects.all()
