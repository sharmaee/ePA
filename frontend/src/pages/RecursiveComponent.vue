<template>
  <div>
    <div>
      <div v-if="parseData.class === 'InteractiveSelect'">
        <fieldset>
          <legend>{{ parseData.legend }}</legend>
          <div v-for="option in parseData.options" :key="option.label">
            <RecursiveComponent :data="option" />
          </div>
        </fieldset>
      </div>

      <div v-else-if="parseData.class === 'InteractiveOption'">
        <div>
          <h3>{{ parseData.label }}</h3>
          <input v-model="parseData.state" type="radio" />
          <div v-if="parseData.state">
            <div v-for="child in parseData.children" :key="child.label">
              <RecursiveComponent :data="child" />
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="data.class === 'CheckListQuestion'">
        <div>
          <h4>{{ data.question }}</h4>
          <input v-model="parseData.value" type="checkbox" />

          <div v-if="parseData.subchecklist">
            <div v-for="subQuestion in parseData.subchecklist" :key="subQuestion.question_or">
              <RecursiveComponent :data="subQuestion" />
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="parseData.class === 'SubCheckListQuestion'">
        <div>
          <span>{{ parseData.question_or }}</span>
          <input v-model="parseData.value_or" type="checkbox" />
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
