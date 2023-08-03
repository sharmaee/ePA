<template>
  <div class="recursive-wrapper">
    <input
      v-if="parseData.nodeType === 'radio'"
      :id="parseData.label"
      v-model="parseData.nodeValue"
      :checked="isChecked"
      :type="parseData.nodeType"
      :value="parseData.nodeValue"
      @click="emit('selectedTerm', parseData.children)" />
    <input
      v-else-if="parseData.nodeType === 'checkbox'"
      :id="parseData.label"
      v-model="parseData.nodeValue"
      :checked="isChecked"
      :type="parseData.nodeType"
      :value="isChecked" />
    <label
      :for="parseData.label"
      :class="{ red: parseData.nodeValue === false && !props.childCheckboxes && buttonClicked }">
      {{ parseData.label }}
    </label>

    <div v-if="parseData.children && parseData.nodeType === 'checkbox'">
      <div v-for="child in parseData.children" :key="child.label" class="offset">
        <RecursiveComponent :data="child" :child-checkboxes="true" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import RecursiveComponent from "@/pages/RecursiveComponent";

const emit = defineEmits(["selectedTerm"]);
const parseData = ref({});

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  childCheckboxes: {
    type: Boolean,
    default: false,
  },
  buttonClicked: {
    type: Boolean,
    default: false,
  },
});

// eslint-disable-next-line vue/no-setup-props-destructure
parseData.value = props.data;

const isChecked = computed(() => {
  if (parseData.value.nodeType === "checkbox" && parseData.value.children && parseData.value.allRequired) {
    return parseData.value.children.every((child) => child.nodeValue === true);
  }
  if (parseData.value.nodeType === "checkbox" && parseData.value.children) {
    return parseData.value.children.some((child) => child.nodeValue === true);
  }
  return parseData.value.nodeValue;
});

watch(isChecked, (newValue) => {
  parseData.value.nodeValue = newValue;
});
</script>

<style lang="scss" scoped>
@import "../styles/pages/_recursive-component.scss";
</style>
