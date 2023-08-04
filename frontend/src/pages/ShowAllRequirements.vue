<!-- TODO
do not show label for nodes with nodeType === 'fieldset'
show children of nodes with nodeType === 'fieldset'
for nodes with nodeType === 'radio' show label and no input
show children of nodes with nodeType === 'radio'
for nodes with nodeType === 'checkbox' show label and input
use ShowCheckList.vue as a template
-->
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
