<template>
  <div class="checklist-wrapper">
    <div v-if="!selectedData">
      <h3>{{ checkListChild.label }}</h3>
      <div v-for="option in checkListChild.children" :key="option.label">
        <QuestionnaireRecursiveComponent :data="option" @selected-term="selectedTerm" />
      </div>
    </div>
    <div v-else>
      <h3 v-if="selectedData[0].nodeType === 'fieldset'"></h3>
      <div
        v-for="(item, listIndex) in selectedData[0].nodeType === 'fieldset' ? selectedData[0].children : selectedData"
        :key="item.label">
        <span :class="{ hide: step !== listIndex }">
          <QuestionnaireRecursiveComponent
            :current-index="listIndex"
            :total-number-steps="
              selectedData[0].nodeType === 'fieldset' ? selectedData[0].children.length : selectedData.length
            "
            :data="item"
            :button-clicked="buttonClicked"
            :step="step"
            @selected-term="selectedTerm"
            @show-next-step="nextStep" />
        </span>
      </div>
      <button v-if="step === selectedData.length - 1" @click="submitChecklist">Submit</button>
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
const buttonClicked = ref(false);

// eslint-disable-next-line vue/no-setup-props-destructure
checkListChild.value = props.data;

function selectedTerm(item) {
  selectedData.value = item;
}

function nextStep() {
  if (step.value < selectedData.value.length - 1) {
    step.value++;
  }
}

const emit = defineEmits(["filterComorbidityData"]);
const filterComorbidityData = (comorbidityData) => emit("filterComorbidityData", comorbidityData);

function submitChecklist() {
  const elementsWithComorbidity = document.getElementsByClassName("comorbidity");
  const comorbidityContentArray = Array.from(elementsWithComorbidity).map((element) => element.textContent);

  comorbidityContentArray.push("Obesity");

  filterComorbidityData(comorbidityContentArray);
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-page.scss";
</style>
