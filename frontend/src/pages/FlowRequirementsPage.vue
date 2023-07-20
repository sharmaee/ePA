<template>
  <PriorHeader />
  <div class="graph-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <p>
      {{ graphData }}
    </p>

    <button v-if="!preloader" class="switch-map" @click="mapSwitcher">{{ showMap }}</button>

    <GreenCirclePreloader v-if="preloader" />

    <div id="graph-wrapper" :class="{ hidden: showMap === 'analog' }" class="graph-wrapper"></div>

    <div :class="{ hidden: showMap === 'graph' }" class="questionaire-wrapper">
      <RecursiveComponent :data="parsedData" />
    </div>
  </div>

  <PriorFooter />
</template>

<script setup>
import { onMounted, ref, reactive } from "vue";
import { instance } from "@viz-js/viz";
import { useRoute } from "vue-router";
import { mainServices } from "@/services/mainServices";

import PriorFooter from "@/components/PriorFooter";
import PriorHeader from "@/components/PriorHeader";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import RecursiveComponent from "@/pages/RecursiveComponent";

const graphContainer = ref(null);
const route = useRoute();
const showMap = ref("graph");

const graphData = ref(null);
const preloader = ref(false);

onMounted(() => {
  graphContainer.value = document.getElementById("graph-wrapper");
  if (route.params.id) {
    getPriorAuthRequirements(route.params.id);
  }
});

async function getPriorAuthRequirements(id) {
  preloader.value = true;
  graphData.value = await mainServices.getGraphData(id);

  instance().then(function (viz) {
    graphContainer.value.appendChild(viz.renderSVGElement(`${graphData.value.requirementsFlow}`));
    let graph = document.getElementsByTagName("svg")[0];
    graph.style.width = 900 + "pt";
    graph.style.height = 550 + "pt";
  });

  preloader.value = false;
}
function mapSwitcher() {
  showMap.value = showMap.value === "graph" ? "analog" : "graph";
  console.log(showMap.value);
}

const parsedData = reactive({
  class: "InteractiveSelect",
  legend: "Start or continue",
  type: "fieldset",
  options: [
    {
      class: "InteractiveOption",
      label: "Start",
      type: "radio",
      state: false,
      children: [
        {
          class: "InteractiveSelect",
          legend: "Age of patient starting therapy",
          type: "fieldset",
          options: [
            {
              class: "InteractiveOption",
              label: "Age 12 to 17 y.o.",
              type: "radio",
              state: false,
              children: [
                {
                  class: "CheckListQuestion",
                  question: "Treatment is being requested for appetite suppression or weight loss",
                  type: "checkbox",
                  value: false,
                },
                {
                  class: "CheckListQuestion",
                  question: "One of the following",
                  type: "checkbox",
                  value: false,
                  subchecklist: [
                    {
                      class: "SubCheckListQuestion",
                      question_or: "Body Mass Index (BMI) ≥ 30 kg/m2 or for pediatric patients a BMI > 95th percentile",
                      type: "checkbox",
                      value_or: false,
                    },
                    {
                      class: "SubCheckListQuestion",
                      question_or:
                        "BMI ≥ 27 kg/m2 and patient has a weight-related comorbidity (e.g., dyslipidemia, hypertension, type 2 diabetes, sleep apnea)",
                      type: "checkbox",
                      value_or: false,
                    },
                  ],
                },
              ],
            },
            {
              class: "InteractiveOption",
              label: "Age >18 y.o.",
              type: "radio",
              state: false,
              children: [
                {
                  class: "CheckListQuestion",
                  question: "Treatment is being requested for appetite suppression or weight loss",
                  type: "checkbox",
                  value: false,
                },
                {
                  class: "CheckListQuestion",
                  question: "One of the following",
                  type: "checkbox",
                  value: false,
                  subchecklist: [
                    {
                      class: "SubCheckListQuestion",
                      question_or: "Body Mass Index (BMI) ≥ 30 kg/m2 or for pediatric patients a BMI > 95th percentile",
                      type: "checkbox",
                      value_or: false,
                    },
                    {
                      class: "SubCheckListQuestion",
                      question_or:
                        "BMI ≥ 27 kg/m2 and patient has a weight-related comorbidity (e.g., dyslipidemia, hypertension, type 2 diabetes, sleep apnea)",
                      type: "checkbox",
                      value_or: false,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
    {
      class: "InteractiveOption",
      label: "Continue",
      type: "radio",
      state: false,
      children: [
        {
          class: "InteractiveSelect",
          legend: "Age of patient continuing therapy",
          type: "fieldset",
          options: [
            {
              class: "InteractiveOption",
              label: "Age 12 to 17 y.o.",
              state: false,
              type: "radio",
              children: [
                {
                  class: "CheckListQuestion",
                  question: "Treatment is being requested for appetite suppression or weight loss",
                  type: "checkbox",
                  value: false,
                },
                {
                  class: "CheckListQuestion",
                  question: "One of the following",
                  type: "checkbox",
                  value: false,
                  subchecklist: [
                    {
                      class: "SubCheckListQuestion",
                      question_or: "Body Mass Index (BMI) ≥ 30 kg/m2 or for pediatric patients a BMI > 95th percentile",
                      type: "checkbox",
                      value_or: false,
                    },
                    {
                      class: "SubCheckListQuestion",
                      question_or:
                        "BMI ≥ 27 kg/m2 and patient has a weight-related comorbidity (e.g., dyslipidemia, hypertension, type 2 diabetes, sleep apnea)",
                      type: "checkbox",
                      value_or: false,
                    },
                  ],
                },
              ],
            },
            {
              class: "InteractiveOption",
              label: "Age >18 y.o.",
              state: false,
              type: "radio",
              children: [
                {
                  class: "CheckListQuestion",
                  question: "Treatment is being requested for appetite suppression or weight loss",
                  type: "checkbox",
                  value: false,
                },
                {
                  class: "CheckListQuestion",
                  question: "One of the following",
                  type: "checkbox",
                  value: false,
                  subchecklist: [
                    {
                      class: "SubCheckListQuestion",
                      question_or: "Body Mass Index (BMI) ≥ 30 kg/m2 or for pediatric patients a BMI > 95th percentile",
                      type: "checkbox",
                      value_or: false,
                    },
                    {
                      class: "SubCheckListQuestion",
                      question_or:
                        "BMI ≥ 27 kg/m2 and patient has a weight-related comorbidity (e.g., dyslipidemia, hypertension, type 2 diabetes, sleep apnea)",
                      type: "checkbox",
                      value_or: false,
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ],
});
</script>

<style lang="sass" scoped>
@import "../styles/pages/_flow-requirements-page"
</style>
