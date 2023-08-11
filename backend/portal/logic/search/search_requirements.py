from portal.models import PriorAuthRequirement


def run_search(search_params):
    search_params = {k + '__trigram_similar': v for k, v in search_params.items() if v is not None and v != ''}
    return PriorAuthRequirement.objects.filter(**search_params).only(
        'url_slug,'
        'description',
        'insurance_provider',
        'insurance_plan_type',
        'insurance_coverage_state',
        'medication',
    )


def get_available_search_options():
    insurance_providers = list(
        PriorAuthRequirement.objects.all().values_list('insurance_provider', flat=True).distinct()
    )
    return {
        "insurance_providers": insurance_providers,
    }
