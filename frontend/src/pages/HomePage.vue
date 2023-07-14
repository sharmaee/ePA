<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <h1>The Wegovy <span class="blue-text">Insurance</span> Navigator.</h1>
    <div class="home-page-main-block">
      <div class="home-page-img">
        <img src="../assets/images/doctor.svg" alt="doctor" />
      </div>
      <div class="home-page-form-wrapper">
        <div class="home-form">
          <h2>Check if you are Eligible for coverage</h2>
          <hr />

          <form action="">
            <div class="insurance-plan-number">
              <label for="insurance-number">Insurance Provider Plan Number*</label>
              <input id="insurance-number" type="text" placeholder="Enter Provider Number" />
            </div>
            <div class="insurance-provider-and-state">
              <div class="insurance-provider">
                <label for="insurance-provider">Insurance Provider*</label>
                <input id="insurance-provider" type="text" placeholder="Insurance provider" />
              </div>
              <div class="insurance-state">
                <label for="insurance-state">Patient Insurance State*</label>
                <input id="insurance-state" type="select" placeholder="City/Area" />
              </div>
            </div>
            <div class="insurance-medication-name">
              <label for="medication-name">Medication Name*</label>
              <input id="medication-name" type="text" placeholder="Search for medication name or NDC number" />
            </div>
            <button @click.prevent="showCoverageBlock" @click="getPriorAuthRequirements">Check My Coverage</button>
          </form>
        </div>

        <div v-if="coverageBlock" class="coverage">
          <div class="request-text">
            <p class="bold">Aetna Commercial Califomia Universal Prescription Drug Prior Authorization</p>
            <p>Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatu</p>
            <div class="coverage-btn-wrapper">
              <a class="btn-blue" href="">start Request</a>
            </div>
          </div>
          <div class="request-text">
            <p class="bold">Aetna Commercial Califomia Universal Prescription Drug Prior Authorization</p>
            <p>Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatu</p>
            <div class="coverage-btn-wrapper">
              <a class="btn-blue" href="">start Request</a>
            </div>
          </div>
          <div class="request-text">
            <p class="bold">Aetna Commercial Califomia Universal Prescription Drug Prior Authorization</p>
            <p>Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatu</p>
            <div class="coverage-btn-wrapper">
              <a class="btn-blue" href="">Start Request</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { mainServices } from "@/services/mainServices";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import { usaStates } from "@/utils/usaStates";
const availableSearchOptions = ref(null);
const priorAuthRequirementsResult = ref(null);

const coverageBlock = ref(false);
let states = [];

onMounted(() => {
  getAvailableSearchOptions();

  for (let stateData of Object.values(usaStates)) {
    states.push(stateData.name);
  }
});

async function getAvailableSearchOptions() {
  availableSearchOptions.value = await mainServices.availableSearchOptions();
}

async function getPriorAuthRequirements() {
  priorAuthRequirementsResult.value = await mainServices.searchRequirements();
}

function showCoverageBlock() {
  coverageBlock.value = true;
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_home-page"
</style>
