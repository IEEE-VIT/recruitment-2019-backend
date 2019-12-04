from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from recruiter.views import RecruiterViewSet
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView

router = routers.DefaultRouter()
router.register(r'users', RecruiterViewSet)


urlpatterns = [
	path('', include(router.urls)),
	path('auth/login/', LoginView.as_view()),
	path('auth/logout/', LogoutView.as_view()),
	path('auth/registration/', RegisterView.as_view())
]
