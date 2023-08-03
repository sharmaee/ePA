<template>
  <div class="checklist-wrapper">
    <div v-if="!selectedData">
      <h3>{{ checkListChild.label }}</h3>
      <div v-for="option in checkListChild.children" :key="option.label">
        <RecursiveComponent :data="option" @selected-term="selectedTerm" />
      </div>
    </div>

    <div v-else>
      <h3 v-if="selectedData[0].nodeType === 'fieldset'">
        {{ selectedData[0].label }}
      </h3>
      <div
        v-for="item in selectedData[0].nodeType === 'fieldset' ? selectedData[0].children : selectedData"
        :key="item.label">
        <RecursiveComponent :data="item" :button-clicked="buttonClicked" @selected-term="selectedTerm" />
      </div>
      <button v-if="selectedData[0].nodeType === 'checkbox'" @click="checkSelectedCheckBoxes">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import { useCheckListStore } from "@/stores/checkListStore";
import { storeToRefs } from "pinia";

const { checkListChild } = storeToRefs(useCheckListStore());
import RecursiveComponent from "@/pages/RecursiveComponent";

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

function checkSelectedCheckBoxes() {
  buttonClicked.value = true;

  for (const obj of selectedData.value) {
    if (obj.hasOwnProperty("nodeValue") && obj.nodeValue === false) {
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_show-checklist.scss";
</style>
