<template>
  <div class="recursive-wrapper">
    <input
      v-if="parseData.nodeType === 'radio'"
      :id="checkboxId"
      v-model="parseData.nodeValue"
      :checked="isChecked"
      :type="parseData.nodeType"
      :value="parseData.nodeValue"
      @click="emit('selectedTerm', { item: parseData.children, smartEngineKey: parseData.smartEngine })" />
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
        diagnosis: parseData.diagnosis && isChecked,
        'radio-label': parseData.nodeType === 'radio',
      }">
      {{ parseData.label }}
    </label>

    <div v-if="parseData.children && parseData.nodeType === 'checkbox'">
      <div v-for="child in parseData.children" :key="child.label" class="offset">
        <QuestionnaireRecursiveComponent :data="child" :child-checkboxes="true" />
      </div>
    </div>

    <button
      v-if="props.currentIndex < props.totalNumberSteps - 1 && parseData.nodeType === 'checkbox' && parseData.children"
      @click="showNextStep">
      Show Next
    </button>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import QuestionnaireRecursiveComponent from "@/pages/QuestionnaireRecursiveComponent";
import { generateRandom4DigitNumber } from "@/utils";

const parseData = ref(props.data);
const step = ref(props.step);

const checkboxId = generateRandom4DigitNumber();

const emit = defineEmits(["selectedTerm", "showNextStep"]);

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
  totalNumberSteps: {
    type: Number,
    default: 0,
  },
  step: {
    type: Number,
    default: 0,
  },
});

watch(
  () => props.step,
  (newStep) => {
    step.value = newStep;
  }
);

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

function showNextStep() {
  emit("showNextStep", step.value);
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-recursive-component.scss";
</style>
