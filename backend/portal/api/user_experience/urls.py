from django.urls import path

from .views import LeaveUXFeedbackView

ux_urls = [
    path('', LeaveUXFeedbackView.as_view()),
]
