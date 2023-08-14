from django.db import models
from portal.models._common import PortalModelBase


class PriorAuthDenial(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    cover_my_meds_key = models.TextField(blank=True, null=True)
    ma_email = models.TextField(blank=True, null=True)
