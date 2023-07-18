from django.urls import path

from .views import LeaveUXFeedbackView, RequestUnavailableRequirementsView

ux_urls = [
    path('', LeaveUXFeedbackView.as_view()),
    path('request-requirements/', RequestUnavailableRequirementsView.as_view()),
]
