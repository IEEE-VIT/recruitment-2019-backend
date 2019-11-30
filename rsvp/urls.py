from django.urls import path

from .views import RsvpView


app_name = "rsvp"

urlpatterns = [
    path('rsvp', RsvpView.as_view()),
]