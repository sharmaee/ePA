from portal.logic.load_csv_data.common import read_data_from_csv, get_raw_requirements
from portal.models._common import slugify, custom_bulk_update_or_create
from portal.models.requirements import PriorAuthRequirement


HEADER_FIELDS = [
    'medication',
    'provider',
    'plan_type',
    'state',
]


def get_cleaned_requirements(requirements):
    requirements_cleaned = {}
    for r in requirements:
        states = r['state'].split('; ')
        for state in states:
            insurance_plan_types = r['plan_type'].split('; ')
            for plan_type in insurance_plan_types:
                url_slug = slugify(r['medication'] + '_' + r['provider'] + '_' + plan_type + '_' + state)
                requirements_cleaned[url_slug] = get_requirement_dict(
                    url_slug, plan_type, state, r['provider'], r['medication']
                )
    return requirements_cleaned


def get_requirement_dict(url_slug, plan_type, state, provider, medication):
    description = (
        f'{provider} Prior Authorization Requirements for {medication} in the state of {state}'
        if state
        else f'{provider} Prior Authorization Requirements for {medication}'
    )
    return {
        'url_slug': url_slug,
        'medication_id': medication,
        'description': description,
        'insurance_provider': provider,
        'insurance_plan_type': plan_type,
        'insurance_coverage_state': state,
    }


def generate_pa_requirements_objects():
    csv_data = read_data_from_csv('portal/fixtures/data/raw_data/prior_auth_requirements.csv')
    requirements = get_raw_requirements(csv_data, HEADER_FIELDS, 'Drug')
    requirements_cleaned = get_cleaned_requirements(requirements)

    existing_requirements = PriorAuthRequirement.objects.values_list("url_slug", flat=True)
    updated_fields = [
        'medication_id',
        'description',
        'insurance_provider',
        'insurance_plan_type',
        'insurance_coverage_state',
    ]
    custom_bulk_update_or_create(
        requirements_cleaned, PriorAuthRequirement, existing_requirements, 'url_slug', updated_fields
    )
