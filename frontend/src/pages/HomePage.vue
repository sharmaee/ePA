<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator</h1>
    <div class="home-page-main-block">
      <div class="home-page-img">
        <img src="../assets/images/woman-with-stethoscope.png" alt="doctor" />
      </div>
      <div class="home-page-form-wrapper">
        <div class="home-form">
          <h2>Check if you are Eligible for coverage</h2>
          <hr />

          <form action="">
            <div class="insurance-provider-and-state">
              <div class="insurance-plan-number">
                <label for="insurance-provider">Insurance Provider*</label>
                <input
                  id="insurance-provider"
                  v-model="userFormData.insuranceProvider"
                  type="text"
                  placeholder="Insurance provider" />
              </div>
              <div class="insurance-state">
                <label for="insurance-state">Patient Insurance State*</label>
                <select
                  id="insurance-state"
                  v-model="userFormData.insuranceCoverageState"
                  class="custom-select-arrow"
                  placeholder="City/Area">
                  <option v-for="state in states" :key="state">{{ state }}</option>
                </select>
              </div>
            </div>

            <div class="insurance-provider">
              <label for="insurance-number">Insurance Provider Plan Number*</label>
              <input
                id="insurance-number"
                v-model="userFormData.insurancePlanNumber"
                type="text"
                placeholder="Enter Provider Number" />
            </div>
            <div class="insurance-medication-name">
              <label for="medication-name">Medication Name*</label>
              <input
                id="medication-name"
                v-model="userFormData.medication"
                type="text"
                placeholder="Search for medication name or NDC number" />
            </div>
            <button @click.prevent="getPriorAuthRequirements">Check My Coverage</button>
          </form>
        </div>
      </div>
    </div>
    <div v-if="coverageBlock" class="coverage">
      <div v-for="item in priorAuthRequirementsResult" :key="item.requirementsFlow" class="request-text">
        <p class="bold">{{ item.insuranceProvider }}</p>
        <p>{{ item.description }}</p>
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
import { onMounted, ref } from "vue";
import { mainServices } from "@/services/mainServices";
import { usaStates } from "@/utils/usaStates";

import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";

const priorAuthRequirementsResult = ref(null);

// not used yet for auto-filling
const availableSearchOptions = ref(null);

const coverageBlock = ref(false);
const preloader = ref(false);
const errMessage = ref(null);

const userFormData = ref({
  insuranceProvider: null,
  insurancePlanNumber: null,
  insuranceCoverageState: null,
  medication: "Wegovy",
});
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

async function getPriorAuthRequirements() {
  preloader.value = true;
  window.scrollTo({
    top: 1000,
    behavior: "smooth",
  });
  try {
    priorAuthRequirementsResult.value = await mainServices.searchRequirements(userFormData.value);
    preloader.value = false;
    coverageBlock.value = true;
  } catch (err) {
    preloader.value = false;
    errMessage.value = err;
  }
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_home-page"
</style>
