from portal.models import PriorAuthRequirement


def run_search(search_params):
    search_params = {k + '__trigram_similar': v for k, v in search_params.items() if v is not None or v != ''}
    return PriorAuthRequirement.objects.filter(**search_params)


def get_available_search_options():
    available = PriorAuthRequirement.objects.all()
    insurance_providers = list(available.values_list('insurance_provider', flat=True).distinct())
    insurance_plan_numbers = list(available.values_list('insurance_plan_number', flat=True).distinct())
    insurance_coverage_states = list(available.values_list('insurance_coverage_state', flat=True).distinct())
    medications = list(available.values_list('medication', flat=True).distinct())
    insurance_plans_by_provider = {}
    for provider in insurance_providers:
        insurance_plans_by_provider[provider.lower()] = list(
            available.filter(insurance_provider=provider).values_list('insurance_plan_number', flat=True).distinct()
        )
    return {
        "insurance_providers": insurance_providers,
        "insurance_plan_numbers": insurance_plan_numbers,
        "insurance_coverage_states": insurance_coverage_states,
        "medications": medications,
        "insurance_plans_by_provider": insurance_plans_by_provider,
    }
