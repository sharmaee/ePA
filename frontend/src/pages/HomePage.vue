<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <h1 :class="{ hide: screenWidth < 835 }">The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <div class="home-page-main-block">
      <div class="home-page-img">
        <img src="../assets/images/woman-with-stethoscope.png" alt="doctor" />
        <div class="shadow-ellipse"></div>
      </div>
      <div :class="{ hide: screenWidth > 835 }" class="h1-wrapper">
        <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
      </div>

      <div class="home-page-form-wrapper">
        <div class="shadow-ellipse"></div>
        <div class="home-form">
          <h2>Check if you are Eligible for coverage</h2>
          <hr />
          <div class="form">
            <div class="insurance-provider-and-state">
              <div class="insurance-plan-number">
                <label for="insurance-provider">Insurance Provider*</label>
                <input
                  id="insurance-provider"
                  v-model="searchFormData.insuranceProvider"
                  type="text"
                  placeholder="Insurance provider" />
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
                  placeholder="City/Area">
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
                placeholder="Search for medication name or NDC number" />
              <span v-if="!isMedicationValid && formButtonClicked" class="input-error-notification">
                Please enter ALL fields to search.
              </span>
            </div>
            <button @click.prevent="getPriorAuthRequirements">Check My Coverage</button>
          </div>
        </div>
      </div>
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
    <GreenCirclePreloader v-else-if="preloader" />
    <p v-else-if="errMessage">Try it later please: {{ errMessage }}</p>
  </div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { mainServices } from "@/services/mainServices";
import { usaStates } from "@/utils/usaStates";
import { storeToRefs } from "pinia";
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
    preloader.value = true;
    window.scrollTo({
      top: 1000,
      behavior: "smooth",
    });
    try {
      priorAuthRequirementsResult.value = await mainServices.searchRequirements(searchFormData.value);
      preloader.value = false;
      coverageBlock.value = true;
      clearTheForm();
    } catch (err) {
      clearTheForm();
      preloader.value = false;
      errMessage.value = err;
    }
  }
}

function clearTheForm() {
  searchFormData.value.insuranceProvider = "";
  searchFormData.value.insuranceCoverageState = "";
  searchFormData.value.medication = "";
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_home-page"
</style>
