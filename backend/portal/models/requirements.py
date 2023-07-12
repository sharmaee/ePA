from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchRank
from django.db import models
from django.db.models import F


from ._common import PortalModelBase, SearchQuerySet, prep_search_query


class PriorAuthRequirement(PortalModelBase):
    insurance_provider = models.TextField()
    insurance_plan_number = models.TextField()
    insurance_coverage_state = models.TextField()
    medication = models.TextField()
    requirements_flow = models.TextField()
