from django.urls import path

from .views import (
    PriorAuthRequirementsView,
    PriorAuthRequirementSearchView,
    PriorAuthRequirementDetailView,
    RequestNewPriorAuthRequirementsView,
)

requirements_urls = [
    path('', PriorAuthRequirementsView.as_view()),
    path('search/', PriorAuthRequirementSearchView.as_view()),
    path('detail/<slug:url_slug>/', PriorAuthRequirementDetailView.as_view()),
    path('request-requirements/', RequestNewPriorAuthRequirementsView.as_view()),
]
