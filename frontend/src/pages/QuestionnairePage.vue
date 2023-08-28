<template>
  <div class="checklist-wrapper">
    <div v-if="!selectedData">
      <h3>{{ checkListChild.label }}</h3>
      <div v-for="option in checkListChild.children" :key="option.label">
        <QuestionnaireRecursiveComponent :data="option" @selected-term="selectedTerm" />
      </div>
    </div>

    <div v-else>
      <h3 v-if="selectedData[0].nodeType === 'fieldset'">
        {{ selectedData[0].label }}
      </h3>
      <div
        v-for="item in selectedData[0].nodeType === 'fieldset' ? selectedData[0].children : selectedData"
        :key="item.label">
        <QuestionnaireRecursiveComponent :data="item" :button-clicked="buttonClicked" @selected-term="selectedTerm" />
      </div>
      <!-- <button v-if="selectedData[0].nodeType === 'checkbox'" @click="checkSelectedCheckBoxes">Submit</button> -->
      <button v-if="selectedData[0].nodeType === 'checkbox'" @click="submitChecklist">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import { useCheckListStore } from "@/stores/checkListStore";
import { storeToRefs } from "pinia";

const { checkListChild } = storeToRefs(useCheckListStore());
import QuestionnaireRecursiveComponent from "@/pages/QuestionnaireRecursiveComponent";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

// eslint-disable-next-line vue/no-setup-props-destructure
checkListChild.value = props.data;

const selectedData = ref(null);
const buttonClicked = ref(false);

function selectedTerm(item) {
  selectedData.value = item;
}

// function checkSelectedCheckBoxes() {
//   buttonClicked.value = true;

//   for (const obj of selectedData.value) {
//     if (obj.hasOwnProperty("nodeValue") && obj.nodeValue === false) {
//     }
//   }
// }

const emit = defineEmits(["showSmartEngine"]);
const showSmartEngine = (comorbidityData) => emit("showSmartEngine", comorbidityData);

function submitChecklist() {
  const elementsWithComorbidity = document.getElementsByClassName("comorbidity");
  const comorbidityContentArray = Array.from(elementsWithComorbidity).map((element) => element.textContent);

  // Add "Objesty" to filters by default
  comorbidityContentArray.push("Obesity");

  showSmartEngine(comorbidityContentArray);
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-page.scss";
</style>
