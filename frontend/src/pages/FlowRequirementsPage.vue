<template>
  <PriorHeader />
  <div id="graph-page-wrapper" class="graph-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <p>
      Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id es Sed ut
      perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, to
    </p>
  </div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useFlowRequirements } from "@/stores";
import { storeToRefs } from "pinia";
import { instance } from "@viz-js/viz";
import { onBeforeRouteLeave } from "vue-router";

import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

const { flowRequirements } = storeToRefs(useFlowRequirements());
const graphContainer = ref(null);

onMounted(() => {
  graphContainer.value = document.getElementById("graph-page-wrapper");
  getPriorAuthRequirements();
});

async function getPriorAuthRequirements() {
  instance().then(function (viz) {
    graphContainer.value.appendChild(viz.renderSVGElement(`${flowRequirements.value}`));
    let graph = document.getElementsByTagName("svg")[0];
    graph.style.width = 900 + "pt";
    graph.style.height = 550 + "pt";
  });
}

onBeforeRouteLeave(() => {
  flowRequirements.value = null;
});
</script>

<style lang="sass" scoped>
@import "../styles/pages/_flow-requirements-page"
</style>
