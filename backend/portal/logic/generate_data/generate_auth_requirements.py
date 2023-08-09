from portal.models._common import slugify
import json


HEADER_FIELDS = [
    'medication',
    'provider',
    'plan_type',
    'state',
    'graph',
    'checklist',
    'file_location',
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
    requirements_cleaned = []
    for r in requirements:
        states = r['state'].split('; ')
        for state in states:
            insurance_plan_types = r['plan_type'].split('; ')
            for plan_type in insurance_plan_types:
                slug = slugify(r['medication'] + '_' + r['provider'] + '_' + plan_type + '_' + state)
                checklist = (read_data_from_json('portal/fixtures' + r['checklist']) if r['checklist'] else "")
                graph = (read_data_from_json('portal/fixtures' + r['graph']) if r['graph'] else "")
                requirements_dict = get_requirement_dict(
                    slug, plan_type, state, graph, checklist, r['provider'], r['file_location']
                )
                requirements_cleaned.append(requirements_dict)
    for i, requirement in enumerate(requirements_cleaned):
        requirement['pk'] = i + 1
    return requirements_cleaned


def write_requirements(requirements):
    with open('portal/fixtures/requirements.json', 'w') as f:
        f.write(json.dumps(requirements, indent=4))


def get_requirement_dict(url_slug, plan_type, state, graph, checklist, provider, file_location):
    return {
        'model': 'portal.PriorAuthRequirement',
        'fields': {
            'url_slug': url_slug,
            'insurance_provider': provider,
            'insurance_plan_type': plan_type,
            'insurance_coverage_state': state,
            'requirements_flow': graph,
            'requirements_checklist': checklist,
            'requirements_flow_file_location': file_location,
        },
    }


def generate_requirements_fixture():
    raw_data = read_data_from_csv()
    requirements = get_raw_requirements(raw_data)
    requirements_cleaned = get_cleaned_requirements(requirements)
    write_requirements(requirements_cleaned)
