<template>
  <PriorHeader />
  <div class="graph-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <p v-if="requirementsData && requirementsData.description">
      {{ requirementsData.description }}
    </p>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div class="shadow-ellipse shadow-ellipse-left"></div>

    <div v-if="!preloader" class="tabs-container">
      <b-button-group>
        <b-button class="switch-tab" :class="{ 'active-tab': activeTab === 'graph' }" @click="activeTab = 'graph'">
          Graph
        </b-button>
        <b-button
          class="switch-tab"
          :class="{ 'active-tab': activeTab === 'questionnaire' }"
          @click="activeTab = 'questionnaire'">
          Questionnaire
        </b-button>
        <b-button
          class="switch-tab"
          :class="{ 'active-tab': activeTab === 'checklist' }"
          @click="activeTab = 'checklist'">
          Checklist
        </b-button>
      </b-button-group>
    </div>

    <GreenCirclePreloader v-if="preloader" />

    <div id="graph-wrapper" :class="{ hidden: activeTab !== 'graph' }" class="graph-wrapper">
      <img
        v-if="requirementsData && requirementsData.requirementsFlowFileLocation"
        :src="`${s3StorageUrl}${requirementsData.requirementsFlowFileLocation}`"
        alt="graph"
        class="graph-image-from-file" />
    </div>
    <div
      v-if="requirementsData && requirementsData.requirementsChecklist"
      :class="{ hidden: activeTab !== 'questionnaire' }"
      class="questionaire-wrapper">
      <QuestionnairePage :data="requirementsData.requirementsChecklist" />
    </div>
    <div
      v-if="requirementsData && requirementsData.requirementsChecklist"
      :class="{ hidden: activeTab !== 'checklist' }"
      class="questionaire-wrapper">
      <ChecklistPage :data="requirementsData.requirementsChecklist" />
    </div>
  </div>

  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
// import { instance } from "@viz-js/viz";
import { useRoute } from "vue-router";
import { mainServices } from "@/services/mainServices";

import PriorFooter from "@/components/PriorFooter";
import PriorHeader from "@/components/PriorHeader";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import QuestionnairePage from "@/pages/QuestionnairePage";
import ChecklistPage from "@/pages/ChecklistPage";

// const graphContainer = ref(null);
const route = useRoute();
const activeTab = ref("graph");
const s3StorageUrl = "https://dopriorauth-portal-public.s3.amazonaws.com";

const requirementsData = ref(null);
const preloader = ref(false);

onMounted(() => {
  // graphContainer.value = document.getElementById("graph-wrapper");
  if (route.params.id) {
    getPriorAuthRequirements(route.params.id);
  }
});

async function getPriorAuthRequirements(id) {
  preloader.value = true;
  requirementsData.value = await mainServices.getRequirementsData(id);

  // instance().then(function (viz) {
  //   graphContainer.value.appendChild(viz.renderSVGElement(`${requirementsData.value.requirementsFlow}`));
  //   let graph = document.getElementsByTagName("svg")[0];
  //   graph.style.width = 900 + "pt";
  //   graph.style.height = 550 + "pt";
  // });

  preloader.value = false;
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_requirements-page"
</style>
