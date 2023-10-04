from portal.models.requirements import InsuranceCoverageCriteria, InsuranceProvider, Medication


def run_search(search_params):
    return InsuranceCoverageCriteria.objects.filter(
        medication__medication__icontains=search_params["medication"],
        insurance_provider__insurance_provider__icontains=search_params["insurance_provider"],
        states__state=search_params["insurance_coverage_state"],
    )


def get_available_search_options():
    insurance_providers = list(InsuranceProvider.objects.all().values_list("insurance_provider", flat=True))
    medications = list(Medication.objects.all().values_list("medication", flat=True))
    return {"insurance_providers": insurance_providers, "medications": medications}
