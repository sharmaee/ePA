<template>
  <PriorHeader />
  <div id="graph-page-wrapper" class="graph-page-wrapper"></div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { mainServices } from "@/services/mainServices";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

import { instance } from "@viz-js/viz";

const availableSearchOptions = ref(null);
const priorAuthRequirementsResult = ref(null);
const dataForGraph = ref(null);
const graphContainer = ref(null);

onMounted(() => {
  graphContainer.value = document.getElementById("graph-page-wrapper");
  getPriorAuthRequirements();
});

availableSearchOptions.value = {
  insurance_provider: "UnitedHealthcare Pharmacy",
  insurance_plan_number: "2023 P 1114-12",
  insurance_coverage_state: "New York",
  medication: "Wegovy",
};

async function getPriorAuthRequirements() {
  priorAuthRequirementsResult.value = await mainServices.searchRequirements(availableSearchOptions.value);
  dataForGraph.value = priorAuthRequirementsResult.value[0].requirementsFlow;

  instance().then(function (viz) {
    graphContainer.value.appendChild(viz.renderSVGElement(dataForGraph.value));
  });
}
</script>

<style lang="sass" scoped></style>
