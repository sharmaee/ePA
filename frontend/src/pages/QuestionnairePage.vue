<template>
  <div class="checklist-wrapper">
    <div v-if="!selectedData">
      <h3>{{ checkListChild.label }}</h3>
      <div v-for="option in checkListChild.children" :key="option.label">
        <QuestionnaireRecursiveComponent :data="option" :current-index="currentIndex" @selected-term="selectedTerm" />
      </div>
    </div>

    <div v-else>
      <h3 v-if="selectedData[0].nodeType === 'fieldset'">
        {{ selectedData[0].label }}
      </h3>
      <div
        v-for="item in selectedData[0].nodeType === 'fieldset' ? selectedData[0].children : selectedData"
        :key="item.label">
        <QuestionnaireRecursiveComponent
          :current-index="currentIndex"
          :data="item"
          :button-clicked="buttonClicked"
          @selected-term="selectedTerm" />
      </div>
      <button v-if="selectedData[0].nodeType === 'checkbox'" @click="submitChecklist">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCheckListStore } from "@/stores/checkListStore";
import { storeToRefs } from "pinia";
import QuestionnaireRecursiveComponent from "@/pages/QuestionnaireRecursiveComponent";

const { checkListChild } = storeToRefs(useCheckListStore());

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const selectedData = ref(null);
const buttonClicked = ref(false);
const currentIndex = ref(0);

// eslint-disable-next-line vue/no-setup-props-destructure
checkListChild.value = props.data;

function selectedTerm(item) {
  selectedData.value = item;
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
