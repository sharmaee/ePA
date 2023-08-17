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
import { defineEmits, defineProps } from "vue";
import ChecklistRecursiveComponent from "@/pages/ChecklistRecursiveComponent";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["show-smart-engine"]);

function submitChecklist() {
  emit("show-smart-engine");
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-page.scss";
</style>
