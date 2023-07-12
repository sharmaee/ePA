from django.urls import path

from .views import PriorAuthRequirementsView, PriorAuthRequirementSearchView

requirements_urls = [
    path('', PriorAuthRequirementsView.as_view()),
    path('search/', PriorAuthRequirementSearchView.as_view()),
]