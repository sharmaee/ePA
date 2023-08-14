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
      v-else-if="parseData.nodeType === 'checkbox'"
      :id="checkboxId"
      v-model="parseData.nodeValue"
      :checked="isChecked"
      :type="parseData.nodeType"
      :value="isChecked" />
    <label :for="checkboxId" :class="{ red: parseData.nodeValue === false && !props.childCheckboxes && buttonClicked }">
      {{ parseData.label }}
    </label>

    <div v-if="parseData.children && parseData.nodeType === 'checkbox'">
      <div v-for="child in parseData.children" :key="child.label" class="offset">
        <QuestionnaireRecursiveComponent :data="child" :child-checkboxes="true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import QuestionnaireRecursiveComponent from "@/pages/QuestionnaireRecursiveComponent";
import { generateRandom4DigitNumber } from "@/utils";

const emit = defineEmits(["selectedTerm"]);
const parseData = ref({});
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
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-recursive-component.scss";
</style>
