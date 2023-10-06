from portal.logic.load_csv_data.common import read_data_from_csv, get_rows_from_csv_data
from portal.models._common import custom_bulk_update_or_create
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
REQUIREMENT_TEMPLATE_FIELDS = ["medication", "requirement_rule_name", "label"]
REQUIREMENT_OPTION_TEMPLATE_FIELDS = ["option_rule_name", "requirement_rule_name", "node_type", "label"]
SMART_ENGINE_FIELDS = ["medication", "requirement_rule_name", "option_rule_name", "label", "validation"]


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
    requirements = get_rows_from_csv_data(csv_data, INSURANCE_COVERAGE_CRITERIA_FIELDS)
    for row in requirements:
        create_requirements_main_reference(row)


def generate_requirement_template_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/requirement_templates.csv")
    requirements = get_rows_from_csv_data(csv_data, REQUIREMENT_TEMPLATE_FIELDS)
    requirement_templates = {}
    for row in requirements:
        medication = Medication.objects.get_or_create(medication=row["medication"])[0]
        requirement = {}
        requirement["requirement_rule_name"] = row["requirement_rule_name"]
        requirement["medication_id"] = medication.pk
        requirement["label"] = row["label"].replace(";", ",")
        requirement_templates[row["requirement_rule_name"]] = requirement
    existing_templates = RequirementTemplate.objects.values_list("requirement_rule_name", flat=True)
    updated_fields = ["label"]
    custom_bulk_update_or_create(
        requirement_templates, RequirementTemplate, existing_templates, "requirement_rule_name", updated_fields
    )


def generate_requirement_option_template_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/requirement_option_templates.csv")
    requirements = get_rows_from_csv_data(csv_data, REQUIREMENT_OPTION_TEMPLATE_FIELDS)
    option_templates = {}
    for row in requirements:
        option = {}
        option["requirement_template_id"] = row["requirement_rule_name"]
        option["option_rule_name"] = row["option_rule_name"]
        option["node_type"] = row["node_type"]
        option["label"] = row["label"].replace(";", ",")
        option_templates[row["option_rule_name"]] = option
    existing_templates = RequirementOptionTemplate.objects.values_list("option_rule_name", flat=True)
    updated_fields = ["label"]
    custom_bulk_update_or_create(
        option_templates, RequirementOptionTemplate, existing_templates, "option_rule_name", updated_fields
    )


def generate_smart_engine_item_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/smart_engine_items.csv")
    requirements = get_rows_from_csv_data(csv_data, SMART_ENGINE_FIELDS)
    for row in requirements:
        medication = Medication.objects.get_or_create(medication=row["medication"])[0]
        SmartEngineItem.objects.create(
            medication=medication,
            requirement_template_id=row["requirement_rule_name"] if row["requirement_rule_name"] else None,
            requirement_option_template_id=row["option_rule_name"] if row["option_rule_name"] else None,
            label=row["label"].replace(";", ","),
            validation=row["validation"].replace(";", ","),
        )
