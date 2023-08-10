from django.urls import path

from .views import LeaveUXFeedbackView, RequestNewRequirementsView

ux_urls = [
    path('', LeaveUXFeedbackView.as_view()),
    path('request-requirements/', RequestNewRequirementsView.as_view()),
]
