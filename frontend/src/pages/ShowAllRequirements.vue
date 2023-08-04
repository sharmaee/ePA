<template>
  <div class="checklist-wrapper">
    <div v-if="props.data && props.data.children">
      <div v-for="option in props.data.children" :key="option.label">
        <CheckListRecursive :data="option" />
      </div>
    </div>
  </div>
</template>

<script setup>
import CheckListRecursive from "@/pages/CheckListRecursive";
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
</script>

<style lang="scss" scoped>
@import "../styles/pages/_show-checklist.scss";
</style>
