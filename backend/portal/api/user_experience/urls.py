from django.urls import path

from .views import LeaveUXFeedbackView, RequestNewPriorAuthRequirementsView

ux_urls = [
    path('', LeaveUXFeedbackView.as_view()),
]
