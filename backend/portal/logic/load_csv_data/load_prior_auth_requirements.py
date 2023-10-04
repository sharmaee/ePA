from portal.logic.load_csv_data.common import read_data_from_csv, get_rows_from_csv_data
from portal.models.requirements import PriorAuthRequirement, State, InsurancePlanType, InsuranceProvider, Medication


HEADER_FIELDS = [
    'medication',
    'provider',
    'plan_type',
    'state',
]


def create_requirements_main_reference(requirement):
    medication = Medication.objects.get_or_create(medication=requirement['medication'])[0]
    insurance_provider = InsuranceProvider.objects.get_or_create(insurance_provider=requirement['provider'])[0]
    requirement_main_reference = PriorAuthRequirement(medication=medication, insurance_provider=insurance_provider)
    requirement_main_reference.save()
    print(requirement_main_reference)
    for state in requirement['state'].split('; '):
        if state is not None:
            print(state)
            s = State.objects.get_or_create(state=state)[0]
            requirement_main_reference.insurance_coverage_states.add(s)
    for plan_type in requirement['plan_type'].split('; '):
        if plan_type is not None:
            print(plan_type)
            p = InsurancePlanType.objects.get_or_create(insurance_plan_type=plan_type)[0]
            requirement_main_reference.insurance_plan_types.add(p)
    requirement_main_reference.save()



def generate_pa_requirements_objects():
    csv_data = read_data_from_csv('portal/fixtures/data/raw_data/prior_auth_requirements.csv')
    requirements = get_rows_from_csv_data(csv_data, HEADER_FIELDS, 'Drug')
    for row in requirements:
        create_requirements_main_reference(row)
