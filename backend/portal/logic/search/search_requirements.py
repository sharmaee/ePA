from portal.models import PriorAuthRequirement


def run_search(search_params):
    return PriorAuthRequirement.objects.filter(**search_params)