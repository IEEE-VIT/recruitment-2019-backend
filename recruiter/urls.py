from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from recruiter.views import RecruiterViewSet

router = routers.DefaultRouter()
router.register(r'users', RecruiterViewSet)


urlpatterns = [
	path('', include(router.urls)),
	path('auth/', include('rest_auth.urls')),
	path('auth/registration/', include('rest_auth.registration.urls'))
]
