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

    <div
      v-if="requirementsData && requirementsData.requirementsChecklist"
      :class="{ hidden: activeTab !== 'questionnaire' }"
      class="questionaire-wrapper">
      <QuestionnairePage :data="requirementsData.requirementsChecklist" @show-smart-engine="showSmartEngine" />
    </div>
    <div
      v-if="requirementsData && requirementsData.requirementsChecklist"
      :class="{ hidden: activeTab !== 'checklist' }"
      class="questionaire-wrapper">
      <ChecklistPage :data="requirementsData.requirementsChecklist" @show-smart-engine="showSmartEngine" />
    </div>
  </div>
  <SmartEngineComponent v-if="smartEngine" />
  <ContentUsefulnessQuestionnaire />
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
import ChecklistPage from "@/pages/ChecklistPage";
import ContentUsefulnessQuestionnaire from "@/components/ContentUsefulnessQuestionnaire";
import SmartEngineComponent from "@/pages/SmartEngineComponent";

const route = useRoute();
const activeTab = ref("questionnaire");

const requirementsData = ref(null);
const preloader = ref(false);
const smartEngine = ref(false);

onMounted(() => {
  if (route.params.id) {
    getPriorAuthRequirements(route.params.id);
  }
});

async function showSmartEngine() {
  window.scrollTo({
    top: 1000,
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
