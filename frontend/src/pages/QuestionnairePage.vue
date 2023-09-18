<template>
  <div class="checklist-wrapper">
    <div v-if="!selectedData">
      <h3>{{ checkListChild.label }}</h3>
      <div v-for="option in checkListChild.children" :key="option.label">
        <QuestionnaireRecursiveComponent :data="option" @selected-term="selectedTerm" />
      </div>
    </div>
    <div v-else>
      <div v-for="(selectedItem, selectedItemIndex) in selectedData" :key="selectedItem.label">
        <h3 :class="{ hide: step !== selectedItemIndex && selectedItem.children[0].nodeType === 'checkbox' }">
          {{ selectedItem.label }}
        </h3>
        <div v-for="subItem in selectedItem.children" :key="subItem.label">
          <span v-if="subItem.nodeType === 'radio'">
            <QuestionnaireRecursiveComponent :data="subItem" @selected-term="selectedTerm" />
          </span>
          <span
            v-if="subItem.nodeType === 'checkbox'"
            :class="{ hide: step !== selectedItemIndex && subItem.nodeType === 'checkbox' }">
            <QuestionnaireRecursiveComponent :data="subItem" :step="step" @selected-term="selectedTerm" />
          </span>
        </div>
        <button
          v-if="step < selectedData.length - 1"
          :class="{ hide: step !== selectedItemIndex }"
          class="next-step-button"
          @click="nextStep">
          Show Next
        </button>
      </div>
      <button v-if="step === selectedData.length - 1 && smartEngineKey" @click="submitChecklist">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCheckListStore } from "@/stores/checkListStore";
import { storeToRefs } from "pinia";
import QuestionnaireRecursiveComponent from "@/pages/QuestionnaireRecursiveComponent";

const { checkListChild } = storeToRefs(useCheckListStore());
const step = ref(0);
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const selectedData = ref(null);
const smartEngineKey = ref(null);

// eslint-disable-next-line vue/no-setup-props-destructure
checkListChild.value = props.data;

function selectedTerm(options) {
  selectedData.value = options.item;
  smartEngineKey.value = options.smartEngineKey;
  if (!selectedData.value && smartEngineKey.value) {
    submitChecklist();
  }
}

function nextStep() {
  if (step.value < selectedData.value.length - 1) {
    step.value++;
  }
}

const emit = defineEmits(["filterSmartEngineData"]);
const filterSmartEngineData = (smartEngineData) => emit("filterSmartEngineData", smartEngineData);

function submitChecklist() {
  const elementsWithDiagnosis = document.getElementsByClassName("diagnosis");
  const diagnosisContentArray = Array.from(elementsWithDiagnosis).map((element) => element.textContent);

  diagnosisContentArray.push("Obesity");

  filterSmartEngineData({ diagnosisContentArray: diagnosisContentArray, smartEngineKey: smartEngineKey.value });
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-page.scss";
</style>
