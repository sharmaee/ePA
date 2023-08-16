<template>
  <div class="checklist-wrapper">
    <div v-if="props.data && props.data.children">
      <div v-for="option in props.data.children" :key="option.label">
        <ChecklistRecursiveComponent :data="option" />
      </div>
    </div>
    <button @click="showSmartEngineContent">Submit</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ChecklistRecursiveComponent from "@/pages/ChecklistRecursiveComponent";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
const smartEngine = ref(false);

function showSmartEngineContent() {
  smartEngine.value = !smartEngine.value;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-page.scss";
</style>
