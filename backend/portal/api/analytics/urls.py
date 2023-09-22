from django.urls import path

from .views import RequirementsSearchActionView

analytics_urls = [
    path('log-requirements-search/', RequirementsSearchActionView.as_view()),
]
