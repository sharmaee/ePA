from portal.logic.load_csv_data.common import read_data_from_csv, get_rows_from_csv_data
from portal.models.requirements import (
    InsuranceCoverageCriteria,
    State,
    InsurancePlanType,
    InsuranceProvider,
    Medication,
    RequirementTemplate,
    RequirementOptionTemplate,
    SmartEngineItem,
)


INSURANCE_COVERAGE_CRITERIA_FIELDS = ["medication", "provider", "plan_type", "state"]
REQUIREMENT_TEMPLATE_FIELDS = ["medication", "rule_name", "label"]
REQUIREMENT_OPTION_TEMPLATE_FIELDS = ["option_rule_name", "requirement_rule_name", "node_type", "label"]
SMART_ENGINE_FIELDS = ["medication", "rule_name", "option_rule_name", "label", "validation"]


def add_missing_records_to_database(model, pk_field, data):
    data_list = list(filter(None, data.split("; ")))
    existing_records = model.objects.filter(**{pk_field + "__in": data_list})
    existing_records_list = list(existing_records.values_list(pk_field, flat=True))
    missing_records = list(set(data_list) - set(existing_records_list))
    model.objects.bulk_create([model(**{pk_field: missing_record}) for missing_record in missing_records])
    return existing_records


def create_requirements_main_reference(requirement):
    medication = Medication.objects.get_or_create(medication=requirement["medication"])[0]
    insurance_provider = InsuranceProvider.objects.get_or_create(insurance_provider=requirement["provider"])[0]
    requirement_main_reference = InsuranceCoverageCriteria(medication=medication, insurance_provider=insurance_provider)
    requirement_main_reference.save()
    states = add_missing_records_to_database(State, "state", requirement["state"])
    requirement_main_reference.states.add(*states)
    plan_types = add_missing_records_to_database(InsurancePlanType, "insurance_plan_type", requirement["plan_type"])
    requirement_main_reference.insurance_plan_types.add(*plan_types)
    requirement_main_reference.save()


def generate_insurance_coverage_criteria_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/prior_auth_requirements.csv")
    requirements = get_rows_from_csv_data(csv_data, INSURANCE_COVERAGE_CRITERIA_FIELDS, "Drug")
    for row in requirements:
        create_requirements_main_reference(row)


def generate_requirement_template_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/requirement_templates.csv")
    requirements = get_rows_from_csv_data(csv_data, REQUIREMENT_TEMPLATE_FIELDS, "Medication")
    for row in requirements:
        medication = Medication.objects.get_or_create(medication=row["medication"])[0]
        RequirementTemplate.objects.create(
            medication=medication, requirement_rule_name=row["rule_name"], label=row["label"]
        )


def generate_requirement_option_template_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/requirement_option_templates.csv")
    requirements = get_rows_from_csv_data(csv_data, REQUIREMENT_OPTION_TEMPLATE_FIELDS, "Option")
    for row in requirements:
        requirement_template = RequirementTemplate.objects.get(requirement_rule_name=row["requirement_rule_name"])
        RequirementOptionTemplate.objects.create(
            requirement_template=requirement_template,
            option_rule_name=row["option_rule_name"],
            node_type=row["node_type"],
            label=row["label"],
        )


def generate_smart_engine_item_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/prior_auth_requirements.csv")
    requirements = get_rows_from_csv_data(csv_data, SMART_ENGINE_FIELDS, "Medication")
    for row in requirements:
        medication = Medication.objects.get_or_create(medication=row["medication"])[0]
        requirement_template = (
            RequirementTemplate.objects.get(requirement_rule_name=row["rule_name"])
            if row["rule_name"] is not None
            else None
        )
        requirement_option_template = (
            RequirementOptionTemplate.objects.get(option_rule_name=row["option_rule_name"])
            if row["option_rule_name"] is not None
            else None
        )
        SmartEngineItem.objects.create(
            medication=medication,
            requirement_template=requirement_template,
            requirement_option_template=requirement_option_template,
            label=row["label"],
            validation=row["validation"],
        )
