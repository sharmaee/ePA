from django.urls import path

from .views import PostUserExperienceView, RequestUnavailableRequirementsView

ux_urls = [
    path('', PostUserExperienceView.as_view()),
    path('request-requirements/', RequestUnavailableRequirementsView.as_view()),
]
