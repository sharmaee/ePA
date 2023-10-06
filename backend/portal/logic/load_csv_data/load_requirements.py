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
    Requirement,
    RequirementOption,
)


INSURANCE_COVERAGE_CRITERIA_FIELDS = ["id", "medication", "provider", "plan_type", "state"]
REQUIREMENT_TEMPLATE_FIELDS = ["medication", "requirement_rule_name", "label"]
REQUIREMENT_OPTION_TEMPLATE_FIELDS = ["option_rule_name", "requirement_rule_name", "node_type", "label"]
SMART_ENGINE_FIELDS = ["medication", "requirement_rule_name", "option_rule_name", "id", "label", "validation"]
REQUIREMENT_OPTION_FIELDS = [
    "id",
    "requirement_rule_name",
    "requirement_rule_set",
    "option_rule_name",
    "option_rule_set",
]


def bulk_get_or_create(model, pk_field, data):
    data_list = list(filter(None, data.split("; ")))
    existing_records = model.objects.filter(**{pk_field + "__in": data_list})
    existing_records_list = list(existing_records.values_list(pk_field, flat=True))
    missing_records = list(set(data_list) - set(existing_records_list))
    model.objects.bulk_create([model(**{pk_field: missing_record}) for missing_record in missing_records])
    return existing_records


def create_or_update_insurance_coverage_criteria(requirement):
    medication = Medication.objects.get_or_create(medication=requirement["medication"])[0]
    insurance_provider = InsuranceProvider.objects.get_or_create(insurance_provider=requirement["provider"])[0]
    requirement_main_reference = InsuranceCoverageCriteria.objects.filter(url_slug=requirement["id"]).first()
    if requirement_main_reference is None:
        requirement_main_reference = InsuranceCoverageCriteria(
            url_slug=requirement["id"], medication=medication, insurance_provider=insurance_provider
        )
        requirement_main_reference.save()
    states = bulk_get_or_create(State, "state", requirement["state"])
    requirement_main_reference.states.add(*states)
    plan_types = bulk_get_or_create(InsurancePlanType, "insurance_plan_type", requirement["plan_type"])
    requirement_main_reference.insurance_plan_types.add(*plan_types)
    requirement_main_reference.save()


def generate_insurance_coverage_criteria_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/prior_auth_requirements.csv")
    requirements = get_rows_from_csv_data(csv_data, INSURANCE_COVERAGE_CRITERIA_FIELDS)
    for row in requirements:
        create_or_update_insurance_coverage_criteria(row)


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
    smart_engine_items = {}
    for row in requirements:
        medication = Medication.objects.get_or_create(medication=row["medication"])[0]
        smart_engine_item = {}
        smart_engine_item["medication_id"] = medication.pk
        smart_engine_item["requirement_template_id"] = row["requirement_rule_name"] if row["requirement_rule_name"] else None
        smart_engine_item["smart_engine_item_id"] = row["id"]
        smart_engine_item["label"] = row["label"].replace(";", ",")
        smart_engine_item["validation"] = row["validation"].replace(";", ",")
        smart_engine_items[row["id"]] = smart_engine_item
    existing_smart_engine_items = SmartEngineItem.objects.values_list("smart_engine_item_id", flat=True)
    updated_fields = ["label", "validation", "requirement_template_id"]
    custom_bulk_update_or_create(
        smart_engine_items, SmartEngineItem, existing_smart_engine_items, "smart_engine_item_id", updated_fields
    )
    for row in requirements:
        smart_engine_item = SmartEngineItem.objects.get(smart_engine_item_id=row["id"])
        option_template_ids = row["option_rule_name"].split("; ")
        option_templates = RequirementOptionTemplate.objects.filter(option_rule_name__in=list(filter(None, option_template_ids)))
        smart_engine_item.requirement_option_template.add(*option_templates)


def generate_requirement_option_objects():
    csv_data = read_data_from_csv("portal/fixtures/data/raw_data/requirements.csv")
    requirements = get_rows_from_csv_data(csv_data, REQUIREMENT_OPTION_FIELDS)
    for row in requirements:
        requirement = Requirement.objects.filter(
            insurance_coverage_criteria_id=row["id"],
            requirement_template_id=row["requirement_rule_name"],
        ).first()
        if requirement is None:
            requirement = Requirement.objects.create(
                insurance_coverage_criteria_id=row["id"],
                requirement_template_id=row["requirement_rule_name"],
            )
        requirement_rules = row["requirement_rule_set"].split("; ")
        requirement_rule_set = RequirementTemplate.objects.filter(requirement_rule_name__in=requirement_rules)
        requirement.requirement_rule_set.add(*requirement_rule_set)
        requirement.save()
        option = RequirementOption.objects.create(
            requirement_id=requirement.pk,
            requirement_option_template_id=row["option_rule_name"],
        )
        option_rules = row["option_rule_set"].split("; ")
        option_rule_set = RequirementOptionTemplate.objects.filter(option_rule_name__in=option_rules)
        option.option_rule_set.add(*option_rule_set)
        option.save()
