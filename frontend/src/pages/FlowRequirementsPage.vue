<template>
  <PriorHeader />
  <div class="graph-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <p v-if="graphData && graphData.description">
      {{ graphData.description }}
    </p>

    <button v-if="!preloader" class="switch-map" @click="mapSwitcher">{{ showMap }}</button>

    <GreenCirclePreloader v-if="preloader" />

    <div id="graph-wrapper" :class="{ hidden: showMap === 'checklist' }" class="graph-wrapper"></div>

    <div
      v-if="graphData && graphData.requirementsChecklist"
      :class="{ hidden: showMap === 'graph' }"
      class="questionaire-wrapper">
      <ShowCheckList :data="graphData.requirementsChecklist" />
    </div>
  </div>

  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { instance } from "@viz-js/viz";
import { useRoute } from "vue-router";
import { mainServices } from "@/services/mainServices";

import PriorFooter from "@/components/PriorFooter";
import PriorHeader from "@/components/PriorHeader";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import RecursiveComponent from "@/pages/RecursiveComponent";
import ShowCheckList from "@/pages/ShowCheckList";

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
  showMap.value = showMap.value === "graph" ? "checklist" : "graph";
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_flow-requirements-page"
</style>
