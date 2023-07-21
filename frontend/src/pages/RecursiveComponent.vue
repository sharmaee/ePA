<template>
  <div>
    <div>
      <div v-if="parseData.class === 'InteractiveSelect'">
        <fieldset>
          <legend>{{ parseData.label }}</legend>
          <div v-for="option in parseData.children" :key="option.label">
            <RecursiveComponent :data="option" />
          </div>
        </fieldset>
      </div>

      <div v-else-if="parseData.class === 'SelectOption'">
        <div>
          <h3>{{ parseData.label }}</h3>
          <input v-model="parseData.value" :type="parseData.type" />
          <div v-if="parseData.type === 'radio' && parseData.value">
            <div v-for="child in parseData.children" :key="child.label">
              <RecursiveComponent :data="child" />
            </div>
          </div>
          <div>
            <div v-if="parseData.type === 'checkbox'">
              <div v-for="child in parseData.children" :key="child.label">
                <RecursiveComponent :data="child" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

import RecursiveComponent from "@/pages/RecursiveComponent";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const parseData = ref({});
// eslint-disable-next-line vue/no-setup-props-destructure
parseData.value = props.data;
</script>

<style lang="scss" scoped></style>
