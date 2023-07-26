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
        :value="parseData.value" />
      <label :for="parseData.label"> {{ parseData.label }}</label>

      <div v-if="parseData.children && parseData.type === 'checkbox'">
        <div v-for="child in parseData.children" :key="child.label" class="offset">
          <RecursiveComponent :data="child" />
        </div>
      </div>
    </div>
  </div>

  <!-- <div class="recursive-wrapper">
    <div v-if="checkListChild.class === 'InteractiveSelect'">
      <fieldset>
        <legend>{{ checkListChild.label }}</legend>
        <div v-for="option in checkListChild.children" :key="option.label">
          <RecursiveComponent :data="option" />
        </div>
      </fieldset>
    </div>

    <div v-else-if="checkListChild.class === 'SelectOption'">
      <h3>{{ checkListChild.label }}</h3>
      <input v-model="checkListChild.value" :type="checkListChild.type" :checked="isChecked" />

      <div v-if="checkListChild.type === 'radio' && checkListChild.value">
        <div v-for="child in checkListChild.children" :key="child.label">
          <RecursiveComponent :data="child" />
        </div>
      </div>

      <div v-else-if="checkListChild.type === 'checkbox'">
        <div v-for="child in checkListChild.children" :key="child.label" class="offset">
          <RecursiveComponent :data="child" />
        </div>
      </div>
    </div>
  </div> -->
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
});

// eslint-disable-next-line vue/no-setup-props-destructure
parseData.value = props.data;

const isChecked = computed(() => {
  if (parseData.value.type === "checkbox" && parseData.value.children) {
    return parseData.value.children.some((child) => child.value === true);
  }
  return false;
});
</script>

<style lang="scss" scoped>
@import "../styles/pages/_recursive-component.scss";
</style>
