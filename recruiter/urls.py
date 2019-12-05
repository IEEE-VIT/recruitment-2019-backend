from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from recruiter.views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'auth', AuthViewSet)

urlpatterns = [
	path('', include(router.urls))
]
