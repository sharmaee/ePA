<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <h1>Prepare Prior Authorizations For <span class="blue-text">Approval</span></h1>

    <div class="home-page-btn-wrapper">
      <router-link :to="{ name: 'insurance-navigator-page' }" class="btn-blue"> Get Started </router-link>
      <router-link :to="{ name: 'request-denial-report' }" class="btn-blue"> Report Denial </router-link>
    </div>
    <div v-if="coverageBlock" class="coverage">
      <div class="request-text missing-requirements-block">
        <span class="bold">
          Missing: {{ searchFormData.insuranceProvider }} {{ searchFormData.insuranceCoverageState }} Wegovy Prior
          Authorization
        </span>
        <span>Let’s get the exact steps you need.</span>
        <div class="coverage-btn-wrapper">
          <router-link :to="{ name: 'request-without-requirements' }" class="btn-blue">
            Request Call for Criteria
          </router-link>
        </div>
      </div>
      <div v-for="item in priorAuthRequirementsResult" :key="item.requirementsFlow" class="request-text">
        <span class="bold">{{ item.insuranceProvider }} | {{ item.insurancePlanType }}</span>
        <span>{{ item.description }}</span>
        <div class="coverage-btn-wrapper">
          <router-link :to="{ name: 'check-my-coverage', params: { id: item.urlSlug } }" class="btn-blue">
            Start Request
          </router-link>
        </div>
      </div>
    </div>
    <GreenCirclePreloader v-if="preloader" />
    <p v-else-if="errMessage">Try it later please: {{ errMessage }}</p>
  </div>
  <PriorFooter />
</template>

<script setup>
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import { useSearchFormStore } from "@/stores/searchFormStore";
const { searchFormData } = storeToRefs(useSearchFormStore());

const priorAuthRequirementsResult = ref(null);
const screenWidth = ref(null);
const formButtonClicked = ref(false);

function displayWindowSize() {
  screenWidth.value = document.documentElement.clientWidth;
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();
// not used yet for auto-filling
const availableSearchOptions = ref(null);

const coverageBlock = ref(false);
const preloader = ref(false);
const errMessage = ref(null);

const states = ref([]);

onMounted(() => {
  getAvailableSearchOptions();

  for (let stateData of Object.values(usaStates)) {
    states.value.push(stateData.name);
  }
});

async function getAvailableSearchOptions() {
  availableSearchOptions.value = await mainServices.availableSearchOptions();
}

// Validators
const isInsuranceProviderValid = computed(() => {
  const value = searchFormData.value.insuranceProvider;
  return value !== null && value.trim() !== "";
});

const isInsuranceCoverageStateValid = computed(() => {
  const value = searchFormData.value.insuranceCoverageState;
  return value !== null && value.trim() !== "";
});

const isMedicationValid = computed(() => {
  const value = searchFormData.value.medication;
  return value !== null && value.trim() !== "";
});

async function getPriorAuthRequirements() {
  formButtonClicked.value = true;

  if (isInsuranceProviderValid.value && isInsuranceCoverageStateValid.value && isMedicationValid.value) {
    coverageBlock.value = false;
    preloader.value = true;
    priorAuthRequirementsResult.value = null;
    window.scrollTo({
      top: 1000,
      behavior: "smooth",
    });
    try {
      priorAuthRequirementsResult.value = await mainServices.searchRequirements(searchFormData.value);
      preloader.value = false;
      coverageBlock.value = true;
    } catch (err) {
      preloader.value = false;
      errMessage.value = err;
    }
  }
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_home-page"
</style>
