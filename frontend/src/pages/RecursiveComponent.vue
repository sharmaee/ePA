<template>
  <div>
    <div class="recursive-wrapper">
      <input
        v-if="parseData.type === 'radio'"
        :id="parseData.label"
        v-model="parseData.value"
        :checked="isChecked"
        :type="parseData.type"
        :value="parseData.value"
        @click="emit('selectedTerm', parseData.children)" />
      <input
        v-else-if="parseData.type === 'checkbox'"
        :id="parseData.label"
        v-model="parseData.value"
        :checked="isChecked"
        :type="parseData.type"
        :value="isChecked" />
      <label
        :for="parseData.label"
        :class="{ red: parseData.value === false && !props.childCheckboxes && buttonClicked }">
        {{ parseData.label }}</label
      >

      <div v-if="parseData.children && parseData.type === 'checkbox'">
        <div v-for="child in parseData.children" :key="child.label" class="offset">
          <RecursiveComponent :data="child" :child-checkboxes="true" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
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
  if (parseData.value.type === "checkbox" && parseData.value.children) {
    // eslint-disable-next-line vue/no-side-effects-in-computed-properties
    parseData.value.value = parseData.value.children.some((child) => child.value === true);
  }
  return parseData.value.value;
});
</script>

<style lang="scss" scoped>
@import "../styles/pages/_recursive-component.scss";
</style>
