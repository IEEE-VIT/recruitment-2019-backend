from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from candidate.views import CandidateViewSet

candidate_list = CandidateViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
candidate_detail = CandidateViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('candidate/', candidate_list, name='candidate-list'),
    path('candidate/<int:pk>/', candidate_detail, name='candidate-detail'),
])