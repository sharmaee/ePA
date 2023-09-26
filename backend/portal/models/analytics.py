from django.db import models
from ._common import PortalModelBase
from portal.models.auth import User


class RequirementsSearchAction(PortalModelBase):
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class RequirementsSearchActionSummary(RequirementsSearchAction):
    class Meta:
        proxy = True
        verbose_name_plural = 'Requirements Search Action Summary'
        verbose_name = 'Requirements Search Action Summary'
        ordering = ['-created_on']


class ServiceEmailLogAction(PortalModelBase):
    class ServiceEmailTypes(models.TextChoices):
        NEW_REQUEST = "More Info Request"
        DENIAL = "Denial Details Submitted"
        PASSWORD_RESET = "Password Reset"
        ACTIVATION = "User Activation"
        NOT_REGISTERED_PROMO = "Domain Not Registered"
        RAN_OUT_OF_SEATS = "Ran Out of Seats"

    email_type = models.TextField(choices=ServiceEmailTypes.choices)
    email_to = models.JSONField()
    email_body = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
