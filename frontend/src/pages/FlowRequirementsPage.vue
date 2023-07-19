<template>
  <PriorHeader />
  <div id="graph-page-wrapper" class="graph-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <p>
      Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id es Sed ut
      perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, to
    </p>
    <GreenCirclePreloader v-if="preloader" />
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

const graphContainer = ref(null);
const route = useRoute();

const graphData = ref(null);
const preloader = ref(false);

onMounted(() => {
  graphContainer.value = document.getElementById("graph-page-wrapper");
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
</script>

<style lang="sass" scoped>
@import "../styles/pages/_flow-requirements-page"
</style>
