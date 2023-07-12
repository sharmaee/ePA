from portal.models import PriorAuthRequirement


def run_search(search_params):
    return PriorAuthRequirement.objects.filter(**search_params)


def get_available_search_options():
    available = PriorAuthRequirement.objects.all()
    insurance_providers = list(available.values_list('insurance_provider', flat=True).distinct())
    insurance_plan_numbers = list(available.values_list('insurance_plan_number', flat=True).distinct())
    insurance_coverage_states = list(available.values_list('insurance_coverage_state', flat=True).distinct())
    medications = list(available.values_list('medication', flat=True).distinct())
    return {
        "insurance_providers": insurance_providers,
        "insurance_plan_numbers": insurance_plan_numbers,
        "insurance_coverage_states": insurance_coverage_states,
        "medications": medications,
    }
