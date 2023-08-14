import json
from portal.models._common import slugify, custom_bulk_update_or_create
from portal.models.requirements import PriorAuthRequirement


HEADER_FIELDS = [
    'medication',
    'provider',
    'plan_type',
    'state',
    'checklist',
]


def read_data_from_csv():
    with open('portal/fixtures/data/raw_data/requirements.csv', 'r') as f:
        raw_data = f.readlines()
    return raw_data


def read_data_from_json(file_path):
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    return json_data


def get_raw_requirements(raw_data):
    requirements = []
    for line in raw_data:
        if line.startswith("Drug"):
            continue
        record = dict(zip(HEADER_FIELDS, line.rstrip('\n').split(',')))
        requirements.append(record)
    return requirements


def get_cleaned_requirements(requirements):
    requirements_cleaned = {}
    for r in requirements:
        states = r['state'].split('; ')
        for state in states:
            insurance_plan_types = r['plan_type'].split('; ')
            for plan_type in insurance_plan_types:
                url_slug = slugify(r['medication'] + '_' + r['provider'] + '_' + plan_type + '_' + state)
                checklist = read_data_from_json('portal/fixtures' + r['checklist']) if r['checklist'] else ""
                requirements_cleaned[url_slug] = get_requirement_dict(
                    url_slug, plan_type, state, checklist, r['provider'], r['medication']
                )
    return requirements_cleaned


def write_requirements(requirements):
    fixture_requirements = []
    for requirement in requirements.values():
        fixture_requirement = {}
        fixture_requirement["model"] = "portal.PriorAuthRequirement"
        fixture_requirement['pk'] = requirement['url_slug']
        fixture_requirement["fields"] = requirement
        fixture_requirements.append(fixture_requirement)
    with open('portal/fixtures/requirements.json', 'w') as f:
        f.write(json.dumps(fixture_requirements, indent=4))


def get_requirement_dict(url_slug, plan_type, state, checklist, provider, medication):
    description = (
        f'{provider} Prior Authorization Requirements for {medication} in the state of {state}'
        if state
        else f'{provider} Prior Authorization Requirements for {medication}'
    )
    return {
        'url_slug': url_slug,
        'medication': medication,
        'description': description,
        'insurance_provider': provider,
        'insurance_plan_type': plan_type,
        'insurance_coverage_state': state,
        'requirements_checklist': checklist,
    }


def generate_requirements_fixture():
    raw_data = read_data_from_csv()
    requirements = get_raw_requirements(raw_data)
    requirements_cleaned = get_cleaned_requirements(requirements)
    write_requirements(requirements_cleaned)


def generate_requirements_objects():
    raw_data = read_data_from_csv()
    requirements = get_raw_requirements(raw_data)
    requirements_cleaned = get_cleaned_requirements(requirements)

    existing_requirements = PriorAuthRequirement.objects.values_list("url_slug", flat=True)
    updated_fields = [
        'medication',
        'description',
        'insurance_provider',
        'insurance_plan_type',
        'insurance_coverage_state',
        'requirements_checklist',
    ]
    custom_bulk_update_or_create(
        requirements_cleaned, PriorAuthRequirement, existing_requirements, 'url_slug', updated_fields
    )
