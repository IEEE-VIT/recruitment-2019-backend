from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from rest_framework import routers

from candidate.views import CandidateListViewSet, CandidateViewSet, ProjectTemplateViewSet

CandidateRouter = routers.DefaultRouter(trailing_slash=False)


CandidateRouter.register(r'candidate/list', CandidateListViewSet, "Candidate List Endpoints")
CandidateRouter.register(r'candidate', CandidateViewSet, "Candidate Modification Endpoints")
CandidateRouter.register(r'project_templates', ProjectTemplateViewSet, "Project Template Endpoints")