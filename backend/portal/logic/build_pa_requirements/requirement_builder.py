from dataclasses import dataclass, asdict, field


@dataclass
class SmartEngineNode:
    label: str
    validation: str


@dataclass
class PriorAuthRequirementsNode:
    node_type: str
    label: str
    smart_engine_checklist: list = field(default_factory=list)


@dataclass
class OptionNode(PriorAuthRequirementsNode):
    rule_name: str
    rule_set: list = field(default_factory=list)
    node_value: bool = False


@dataclass
class FieldsetNode(PriorAuthRequirementsNode):
    node_type = "fieldset"
    question_rule_name: str
    question_rule_set: list = field(default_factory=list)
    children: list[OptionNode] = field(default_factory=list)


@dataclass
class RadioNode(OptionNode):
    node_type = "radio"


@dataclass
class CheckboxNode(OptionNode):
    node_type = "checkbox"
