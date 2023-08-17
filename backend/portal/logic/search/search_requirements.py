from portal.models import PriorAuthRequirement
import datetime


def run_search(search_params):
    return (
        PriorAuthRequirement.objects.filter(medication=search_params['medication'])
        .filter(insurance_coverage_state=search_params['insurance_coverage_state'])
        .filter(insurance_provider__icontains=search_params['insurance_provider'])
        .only(
            "url_slug",
            "description",
            "insurance_provider",
            "insurance_plan_type",
            "insurance_coverage_state",
            "medication",
        )
    )


def get_available_search_options():
    insurance_providers = list(
        PriorAuthRequirement.objects.all().values_list("insurance_provider", flat=True).distinct()
    )
    return {"insurance_providers": insurance_providers}
