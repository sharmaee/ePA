<template>
  <PriorHeader />
  <div class="insurance-navigator-wrapper">
    <h1 :class="{ hide: screenWidth < 835 }">
      Prepare Prior Authorization For <span class="blue-text">Approval</span>
    </h1>
    <div class="insurance-navigator-main-block">
      <div class="insurance-navigator-img">
        <img src="../assets/images/woman-with-stethoscope.png" alt="doctor" />
        <div class="shadow-ellipse"></div>
      </div>
      <div :class="{ hide: screenWidth > 835 }" class="h1-wrapper">
        <h1>Prepare Prior Authorization For <span class="blue-text">Approval</span></h1>
      </div>

      <div class="insurance-navigator-form-wrapper">
        <div class="shadow-ellipse"></div>
        <div class="home-form">
          <h2>Get Prior Authorization Criteria</h2>
          <hr />
          <div class="form">
            <div class="insurance-provider-and-state">
              <div class="insurance-plan-number">
                <label for="insurance-provider">Insurance Provider*</label>
                <input
                  id="insurance-provider"
                  v-model="searchFormData.insuranceProvider"
                  type="text"
                  placeholder="Insurance provider"
                  @keyup="(event) => sendFormByEnterClicking(event, getPriorAuthRequirements)" />
                <span v-if="!isInsuranceProviderValid && formButtonClicked" class="input-error-notification">
                  Please enter ALL fields to search.
                </span>
              </div>
              <div class="insurance-state">
                <label for="insurance-state">Patient Insurance State*</label>
                <select
                  id="insurance-state"
                  v-model="searchFormData.insuranceCoverageState"
                  class="custom-select-arrow"
                  @keyup="(event) => sendFormByEnterClicking(event, getPriorAuthRequirements)">
                  <option v-for="state in states" :key="state">{{ state }}</option>
                </select>
                <span v-if="!isInsuranceCoverageStateValid && formButtonClicked" class="input-error-notification">
                  Please enter ALL fields to search.
                </span>
              </div>
            </div>
            <div class="insurance-medication-name">
              <label for="medication-name">Medication Name*</label>
              <input
                id="medication-name"
                v-model="searchFormData.medication"
                type="text"
                placeholder="Search for medication name or NDC number"
                @keyup="(event) => sendFormByEnterClicking(event, getPriorAuthRequirements)" />
              <span v-if="!isMedicationValid && formButtonClicked" class="input-error-notification">
                Please enter ALL fields to search.
              </span>
            </div>
            <button @click="getPriorAuthRequirements">Get Criteria</button>
          </div>
        </div>
      </div>
    </div>
    <div id="searchResultsBlock"></div>
    <GreenCirclePreloader v-if="preloader" />

    <span id="coverage"></span>
    <div v-if="coverageBlock" class="coverage">
      <div v-if="priorAuthRequirementsResult.length > 0">
        <div v-for="item in priorAuthRequirementsResult" :key="item.requirementsFlow" class="request-text">
          <span class="bold">{{ item.insuranceProvider }} | {{ item.insurancePlanType }}</span>
          <span>{{ item.description }}</span>
          <div class="coverage-btn-wrapper">
            <router-link :to="{ name: 'check-my-coverage', params: { id: item.urlSlug } }" class="btn-blue">
              Get Steps
            </router-link>
          </div>
        </div>
      </div>
      <div v-else class="request-text missing-requirements-block">
        <span class="bold"> Prior Authorization Criteria </span>
        <span> This insurance is not common. The steps will be more precise as we gather more data. </span>
        <div class="coverage-btn-wrapper">
          <router-link :to="{ name: 'check-my-coverage', params: { id: defaultChecklistId } }" class="btn-blue">
            Get Steps
          </router-link>
        </div>
      </div>
    </div>
    <span v-if="errors.length > 0" class="input-error-notification">
      <span v-for="error in errors" :key="error">{{ error }}</span>
    </span>
  </div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { mainServices } from "@/services/mainServices";
import { analyticsServices } from "@/services/analyticsService";
import { usaStates } from "@/utils/usaStates";
import { storeToRefs } from "pinia";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import { useSearchFormStore } from "@/stores/searchFormStore";
const { searchFormData } = storeToRefs(useSearchFormStore());
import { tryParseApiErrors, sendFormByEnterClicking } from "@/utils";
const errors = ref([]);
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

const states = ref([]);

const defaultChecklistId = "8f9e5febd5e6b3fa";

onMounted(() => {
  getAvailableSearchOptions();
  clearTheForm();

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
    preloader.value = true;
    const searchResultsBlock = document.getElementById("searchResultsBlock");
    searchResultsBlock.scrollIntoView({ behavior: "smooth" });
    try {
      coverageBlock.value = false;
      priorAuthRequirementsResult.value = null;
      priorAuthRequirementsResult.value = await mainServices.searchRequirements(searchFormData.value);
      analyticsServices.logRequirementsSearchAction(searchFormData.value);
      preloader.value = false;
      coverageBlock.value = true;
      const coverageBlockView = document.getElementById("coverage");
      coverageBlockView.scrollIntoView({ behavior: "smooth" });
    } catch (err) {
      clearTheForm();
      preloader.value = false;
      errors.value = tryParseApiErrors(err);
    }
  }
}

function clearTheForm() {
  searchFormData.value.insuranceProvider = "";
  searchFormData.value.insuranceCoverageState = "";
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_insurance-navigator-page"
</style>
