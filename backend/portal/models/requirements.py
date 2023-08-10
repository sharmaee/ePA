from django.db import models
from ._common import PortalModelBase


class PriorAuthRequirement(PortalModelBase):
    url_slug = models.TextField(primary_key=True, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    insurance_provider = models.TextField(blank=True, null=True, db_index=True)
    insurance_plan_number = models.TextField(blank=True, null=True, db_index=True)
    insurance_plan_type = models.TextField(blank=True, null=True, db_index=True)
    insurance_coverage_state = models.TextField(blank=True, null=True, db_index=True)
    medication = models.TextField(blank=True, null=True, db_index=True)
    requirements_flow = models.TextField(blank=True, null=True)
    requirements_checklist = models.JSONField(null=True)
    requirements_flow_file_location = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs):
        while not self.url_slug:
            url_slug = self.generate_url_slug()
            if not self.objects.filter(url_slug=url_slug).exists():
                self.url_slug = url_slug
        super().save(*args, **kwargs)
