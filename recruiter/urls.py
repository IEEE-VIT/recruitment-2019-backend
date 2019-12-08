from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from recruiter.views import AuthViewSet, UserViewSet, AvailableRoomViewset

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'auth', AuthViewSet)
router.register(r'users', UserViewSet)
router.register(r'rooms', AvailableRoomViewset)

urlpatterns = [
	path('', include(router.urls))
]
