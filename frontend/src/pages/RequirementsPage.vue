<template>
  <PriorHeader />
  <div class="graph-page-wrapper">
    <div v-if="!successPage" class="reqirements-title-wrapper">
      <h1>Prepare Prior Authorization for <span class="blue-text">Approval</span></h1>
      <p v-if="requirementsData && requirementsData.description">
        {{ requirementsData.description }}
      </p>
    </div>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div class="shadow-ellipse shadow-ellipse-left"></div>

    <GreenCirclePreloader v-if="preloader" />

    <div v-if="requirementsData && requirementsData.requirementsChecklist && !smartEngine" class="questionaire-wrapper">
      <QuestionnairePage
        :data="requirementsData.requirementsChecklist"
        @filter-smart-engine-data="filterSmartEngineData" />
    </div>
  </div>
  <div v-if="smartEngine && !successPage" id="smart-engine-wrapper">
    <SmartEngineComponent
      :diagnosis-filter-data="diagnosisFilterData"
      :step-verify-docs="requirementsData.smartEngineChecklist"
      :smart-engine-key-data="smartEngineKeyData"
      @show-success-engine-page="showSuccessEnginePage" />
  </div>
  <div v-if="successPage">
    <SuccessSmartEnginePage />
  </div>
  <ContentUsefulnessQuestionnaire v-if="smartEngine && !successPage" />
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { mainServices } from "@/services/mainServices";

import PriorFooter from "@/components/PriorFooter";
import PriorHeader from "@/components/PriorHeader";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import QuestionnairePage from "@/pages/QuestionnairePage";
import ContentUsefulnessQuestionnaire from "@/components/ContentUsefulnessQuestionnaire";
import SmartEngineComponent from "@/pages/SmartEngineComponent";
import SuccessSmartEnginePage from "./SuccessSmartEnginePage";

const route = useRoute();

const requirementsData = ref(null);
const preloader = ref(false);
const smartEngine = ref(false);
const smartEngineKeyData = ref(null);
const diagnosisFilterData = ref([]);
const successPage = ref(false);

onMounted(() => {
  if (route.params.id) {
    getPriorAuthRequirements(route.params.id);
  }
});

function snakeToCamel(str) {
  return str.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());
}

async function filterSmartEngineData(options) {
  diagnosisFilterData.value = options.diagnosisContentArray;
  smartEngineKeyData.value = snakeToCamel(options.smartEngineKey);

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });

  smartEngine.value = true;
}

async function getPriorAuthRequirements(id) {
  preloader.value = true;
  requirementsData.value = await mainServices.getRequirementsData(id);
  preloader.value = false;
}

function showSuccessEnginePage() {
  successPage.value = true;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_requirements-page";
</style>
