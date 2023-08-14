from django.urls import path

from .views import SubmitDenialView

denials_urls = [
    path('', SubmitDenialView.as_view()),
]
