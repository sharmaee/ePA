<template>
  <PriorHeader />
  <div class="graph-page-wrapper">
    <h1>Prepare Prior Authorization for <span class="blue-text">Approval</span></h1>
    <p v-if="requirementsData && requirementsData.description">
      {{ requirementsData.description }}
    </p>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div class="shadow-ellipse shadow-ellipse-left"></div>

    <GreenCirclePreloader v-if="preloader" />

    <div v-if="requirementsData && requirementsData.requirementsChecklist && !smartEngine" class="questionaire-wrapper">
      <QuestionnairePage
        :data="requirementsData.requirementsChecklist"
        @filter-comorbidity-data="filterComorbidityData" />
    </div>
  </div>
  <div v-if="smartEngine" id="smart-engine-wrapper">
    <SmartEngineComponent
      :comorbidity-filter-data="comorbidityFilterData"
      :step-verify-docs="requirementsData.smartEngineChecklist" />
  </div>
  <ContentUsefulnessQuestionnaire v-if="smartEngine" />
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

const route = useRoute();

const requirementsData = ref(null);
const preloader = ref(false);
const smartEngine = ref(false);
const comorbidityFilterData = ref([]);

onMounted(() => {
  if (route.params.id) {
    getPriorAuthRequirements(route.params.id);
  }
});

async function filterComorbidityData(comorbidityData) {
  comorbidityFilterData.value = comorbidityData;

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
</script>

<style lang="scss" scoped>
@import "../styles/pages/_requirements-page";
</style>
