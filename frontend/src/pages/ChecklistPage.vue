<template>
  <div class="checklist-wrapper">
    <div v-if="props.data && props.data.children">
      <div v-for="option in props.data.children" :key="option.label">
        <ChecklistRecursiveComponent :data="option" />
      </div>
    </div>
    <button @click="submitChecklist">Submit</button>
  </div>
</template>

<script setup>
import ChecklistRecursiveComponent from "@/pages/ChecklistRecursiveComponent";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

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
