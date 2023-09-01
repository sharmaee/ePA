<template>
  <div class="recursive-wrapper">
    <input
      v-if="parseData.nodeType === 'radio'"
      :id="checkboxId"
      v-model="parseData.nodeValue"
      :checked="isChecked"
      :type="parseData.nodeType"
      :value="parseData.nodeValue"
      @click="emit('selectedTerm', parseData.children)" />
    <input
      v-else-if="parseData.nodeType === 'checkbox' && !parseData.children"
      :id="checkboxId"
      v-model="parseData.nodeValue"
      :checked="isChecked"
      :type="parseData.nodeType"
      :value="isChecked" />
    <label
      :for="checkboxId"
      class="check-box-block-label"
      :class="{
        red: parseData.nodeValue === false && !props.childCheckboxes && buttonClicked,
        comorbidity: parseData.comorbidity && isChecked,
      }">
      {{ parseData.label }}
    </label>

    <div v-if="parseData.children && parseData.nodeType === 'checkbox'">
      <div v-for="child in parseData.children" :key="child.label" class="offset">
        <QuestionnaireRecursiveComponent :data="child" :child-checkboxes="true" />
      </div>
    </div>

    <button v-if="showNextButton && parseData.nodeType === 'checkbox' && parseData.children" @click="showNext">
      Show Next
    </button>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import QuestionnaireRecursiveComponent from "@/pages/QuestionnaireRecursiveComponent";
import { generateRandom4DigitNumber } from "@/utils";

const emit = defineEmits(["selectedTerm"]);
const parseData = ref({});
const currentIndex = ref(0);

const checkboxId = generateRandom4DigitNumber();

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  childCheckboxes: {
    type: Boolean,
    default: false,
  },
  buttonClicked: {
    type: Boolean,
    default: false,
  },
  currentIndex: {
    type: Number,
    default: 0,
  },
});

// eslint-disable-next-line vue/no-setup-props-destructure
parseData.value = props.data;

const isChecked = computed(() => {
  if (parseData.value.nodeType === "checkbox" && parseData.value.children && parseData.value.allRequired) {
    return parseData.value.children.every((child) => child.nodeValue === true);
  }
  if (parseData.value.nodeType === "checkbox" && parseData.value.children) {
    return parseData.value.children.some((child) => child.nodeValue === true);
  }
  return parseData.value.nodeValue;
});

watch(isChecked, (newValue) => {
  parseData.value.nodeValue = newValue;
});

const showNextButton = computed(() => {
  if (parseData.value.nodeType === "checkbox" && parseData.value.children) {
    console.log(props.currentIndex, currentIndex.value);
    return true;
  }
  return false;
});
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-recursive-component.scss";
</style>

<!-- 
DONE -  if nodeType === fieldset show all children (radio) with recursive component
?    -  if nodeType === radio show children one by one with submit button
??   -  pass each child to recursive component
???  -  hide other children until submit is clicked (don’t show next or previous, show next after submit clicked)
DONE -  if nodeType === checkbox show all children offset with recursive component, don’t show input (edited) 
 -->

<!-- {
  "url_slug": "1c9d88ad21b265b0",
  "description": "Kaiser Permanente Prior Authorization Requirements for Wegovy (semaglutide) in the state of California",
  "insurance_provider": "Kaiser Permanente",
  "insurance_plan_type": "Medicaid",
  "insurance_coverage_state": "California",
  "medication": "Wegovy (semaglutide)",
  "requirements_checklist": {
      "label": "Is this request for starting or continued therapy with Wegovy™ (semaglutide)?",
      "children": [
          {
              "label": "Initial review criteria",
              "outcome": "The requested drug, Wegovy™ (semaglutide), is expected to be covered with prior authorization for 3 months",
              "children": [
                  {
                      "label": "Which Weight-Related Risk Factors Does the Patient Have? (Must Have at Least One, Select All That Apply)",
                      "children": [
                          {
                              "label": "Established cardiovascular disease or stroke",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Hypertension",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Type 2 diabetes (DM)",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Chronic kidney disease (CKD)",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Congenital heart disease (CHD)",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Obstructive sleep apnea",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Polycystic ovarian syndrome",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Dyslipidemia",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Non-alcoholic fatty liver disease",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Idiopathic intracranial hypertension",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          },
                          {
                              "label": "Osteoarthritis in weight-bearing joints",
                              "node_type": "checkbox",
                              "node_value": false,
                              "comorbidity": true
                          }
                      ],
                      "node_type": "checkbox",
                      "node_value": false,
                      "all_required": true
                  },
                  {
                      "label": "All of the Below Must Be Tried Before Wegovy for at Least 3 Months Without Losing >5% Body Weight. Do a PA for the Missing Medications in the Order Listed. OR Document Reason They Cannot Be Used (e.g., Side Effects, Contraindication, Adherence).",
                      "children": [
                          {
                              "label": "Xenical (orlistat)",
                              "node_type": "checkbox",
                              "node_value": false
                          },
                          {
                              "label": "Contrave (naltrexone + bupropion)",
                              "node_type": "checkbox",
                              "node_value": false
                          },
                          {
                              "label": "Qsymia (phentermine + topiramate)",
                              "node_type": "checkbox",
                              "node_value": false
                          },
                          {
                              "label": "Saxenda (liraglutide)",
                              "node_type": "checkbox",
                              "node_value": false
                          }
                      ],
                      "node_type": "checkbox",
                      "node_value": false,
                      "all_required": true
                  }
              ],
              "node_type": "radio",
              "node_value": false
          },
          {
              "label": "Continuation of therapy",
              "outcome": "The requested drug, Wegovy™ (semaglutide), is expected to be covered with prior authorization for 6 months",
              "children": [
                  {
                      "label": "Patient continues to meet initial review criteria",
                      "node_type": "checkbox",
                      "node_value": false
                  },
                  {
                      "label": "Documented weight loss within the previous 3 months of at least 10% from baseline weight",
                      "node_type": "checkbox",
                      "node_value": false
                  }
              ],
              "node_type": "radio",
              "node_value": false
          }
      ],
      "node_type": "fieldset"
  },
  "smart_engine_checklist": {
      "items": [
          "The Prescribing Provider Is an Endocrinologist or Weight Management Specialist. If Not, Stop and Ask Clinical Staff to Make a Referral. (This Does Not Require Documentation).",
          "The Patient's Starting Baseline Body Mass Index (BMI) 30 kg/m^2 or Greater",
          "Patient Is 18 Years of Age or Older",
          "Wegovy Is Not Being Used with Another Weight Loss Drug or GLP-1 Receptor Agonist",
          "The Initial Order Is a 30-Day Supply with 2 Refills. When Over This Amount Ask Clinical Staff to Make an Adjustment."
      ],
      "header": "Step 2: Verify Prescriber and Patient Documentation"
  }
} -->
