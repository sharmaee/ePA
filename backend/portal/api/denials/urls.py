from django.urls import path

from .views import SubmitDenialView

ux_urls = [
    path('', SubmitDenialView.as_view()),
]
