from django.urls import path

from .views import (
    PriorAuthRequirementsView,
    PriorAuthRequirementSearchView,
    InsuranceCoverageCriteriaRequirementsView,
    RequestNewPriorAuthRequirementsView,
    PriorAuthSubmissionView,
)

requirements_urls = [
    path('', PriorAuthRequirementsView.as_view()),
    path('search/', PriorAuthRequirementSearchView.as_view()),
    path('detail/<slug:url_slug>/', InsuranceCoverageCriteriaRequirementsView.as_view()),
    path('request-requirements/', RequestNewPriorAuthRequirementsView.as_view()),
    path('complete/', PriorAuthSubmissionView.as_view()),
]
