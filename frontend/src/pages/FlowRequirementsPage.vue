<template>
  <PriorHeader />
  <div id="graph-page-wrapper" class="graph-page-wrapper"></div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useFlowRequirements } from "@/stores";
import { storeToRefs } from "pinia";
import { instance } from "@viz-js/viz";

import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

const { flowRequirements } = storeToRefs(useFlowRequirements());
const graphContainer = ref(null);

onMounted(() => {
  graphContainer.value = document.getElementById("graph-page-wrapper");
  getPriorAuthRequirements();
});

onUnmounted(() => {
  flowRequirements.value = null;
});

async function getPriorAuthRequirements() {
  instance().then(function (viz) {
    graphContainer.value.appendChild(viz.renderSVGElement(`${flowRequirements.value}`));
  });
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_flow-requirements-page"
</style>
