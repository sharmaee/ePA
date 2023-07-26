<template>
  <div>
    <div v-if="checkListChild.class === 'InteractiveSelect' && !selectedData">
      <h3>{{ checkListChild.label }}</h3>
      <div v-for="option in checkListChild.children" :key="option.label">
        <RecursiveComponent :data="option" @selected-term="selectedTerm" />
      </div>
    </div>

    <div v-else-if="selectedData[0].class === 'InteractiveSelect'">
      <h3>{{ selectedData[0].label }}</h3>
      <div v-for="option in selectedData[0].children" :key="option.label">
        <RecursiveComponent :data="option" @selected-term="selectedTerm" />
      </div>
    </div>

    <div v-else-if="selectedData[0].class === 'SelectOption'">
      <div v-for="item in selectedData" :key="item.label">
        <RecursiveComponent :data="item" @selected-term="selectedTerm" />
      </div>
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

function selectedTerm(item) {
  selectedData.value = item;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_show-checklist.scss";
</style>
