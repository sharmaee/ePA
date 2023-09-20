from portal.models.requirements import PriorAuthRequirement
from portal.models.analytics import RequirementsSearchAction


def save_search_action(search_params, user):
    RequirementsSearchAction.objects.create(
        insurance_provider=search_params['insurance_provider'],
        state=search_params['insurance_coverage_state'],
        medication=search_params['medication'],
        created_by=user,
    )


def run_search(search_params, user):
    save_search_action(search_params, user)
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
