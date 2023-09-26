<template>
  <div class="form">
    <div class="row-with-two-input">
      <div class="cover-my-meds-key">
        <label for="cover-my-meds-key">CoverMyMeds Key</label>
        <input
          id="cover-my-meds-key"
          v-model="data.coverMyMedsKey"
          type="text"
          placeholder="B4HL4T2E"
          @keyup="(event) => sendFormByEnterClicking(event, sendRequirements)" />
        <span v-if="!isCoverMyMedsKeyValid && formButtonClicked" class="input-error-notification">
          Please enter a valid CoverMyMeds Key.
        </span>
      </div>
      <div class="patient-last-name">
        <label for="patient-last-name">Patient Last Name</label>
        <input
          id="patient-last-name"
          v-model="data.lastName"
          type="text"
          placeholder="Snow"
          @keyup="(event) => sendFormByEnterClicking(event, sendRequirements)" />
        <span v-if="!isLastNameValid && formButtonClicked" class="input-error-notification">
          Please enter patient last name.
        </span>
      </div>
    </div>

    <div class="row-with-two-input">
      <div class="date-of-birth">
        <label for="date-of-birth">Patient Date Of Birth</label>
        <input
          id="date-of-birth"
          v-model="data.dob"
          type="text"
          placeholder="MM/DD/YYYY"
          @keyup="(event) => sendFormByEnterClicking(event, sendRequirements)" />
        <span v-if="!isDobValid && formButtonClicked" class="input-error-notification">
          Please enter a valid date of birth (MM/DD/YYYY).
        </span>
      </div>
      <div class="patient-member-id">
        <label for="patient-member-id">Patient Member ID</label>
        <input
          id="patient-member-id"
          v-model="data.memberId"
          type="text"
          placeholder="H3485045"
          @keyup="(event) => sendFormByEnterClicking(event, sendRequirements)" />
        <span v-if="!isPatientMemberIdValid && formButtonClicked" class="input-error-notification">
          Please enter a valid member ID.
        </span>
      </div>
    </div>

    <div v-if="route.name === 'request-missing-requirements'">
      <div class="row-with-one-input">
        <div class="patient-member-id">
          <label for="medication-name">Medication Name*</label>
          <select
            id="insurance-state"
            v-model="data.medication"
            class="custom-select-arrow"
            @keyup="(event) => sendFormByEnterClicking(event, getPriorAuthRequirements)">
            <option v-for="medication in medications" :key="medication" :value="medication">{{ medication }}</option>
          </select>
          <span v-if="!isMedicationValid && formButtonClicked" class="input-error-notification">
            Please enter ALL fields to search.
          </span>
        </div>
      </div>
    </div>
    <button @click="sendRequirements">{{ btnText }}</button>
    <br />
    <span v-if="errors.length > 0" class="input-error-notification">
      Sorry, something went wrong. Please contact us at
      <a href="mailto:founders@lamarhealth.com"> founders@lamarhealth.com</a> or try again later
    </span>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { mainServices } from "@/services/mainServices";
import { denialService } from "@/services/denialService";
import { storeToRefs } from "pinia";
import { useSearchFormStore } from "@/stores/searchFormStore";
import { useUiElementsStore } from "@/stores/uiElementsStore";
import { useRoute } from "vue-router";
import { usaStates } from "@/utils/usaStates";
import { tryParseApiErrors, sendFormByEnterClicking } from "@/utils";
const { searchFormData } = storeToRefs(useSearchFormStore());

const route = useRoute();
const states = ref([]);

onMounted(() => {
  for (let stateData of Object.values(usaStates)) {
    states.value.push(stateData.name);
  }
});

const { showPreloader, successModalWindow } = storeToRefs(useUiElementsStore());
const btnText = route.name === "request-missing-requirements" ? "Email me steps" : "Submit";

const formButtonClicked = ref(false);
const errors = ref([]);

const appVersion = process.env.VUE_APP_VERSION;

const data = ref({
  medication: searchFormData.value.medication,
  insuranceProvider: searchFormData.value.insuranceProvider,
  insuranceCoverageState: searchFormData.value.insuranceCoverageState,
  coverMyMedsKey: "",
  lastName: "",
  dob: "",
  memberId: "",
  releaseVersion: appVersion,
});

const medications = ["Saxenda", "Mounjaro", "Ozempic", "Victoza", "Rybelsus", "Wegovy"];

// Validators
const dobPattern = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$/;
const coverMyMedsKeyPattern = /^[A-Za-z0-9]{6,8}$/;
const patientMemberIdPattern = /^[A-Za-z0-9]{3,20}$/;

const isDobValid = computed(() => {
  return dobPattern.test(data.value.dob);
});

const isCoverMyMedsKeyValid = computed(() => {
  return coverMyMedsKeyPattern.test(data.value.coverMyMedsKey);
});

const isPatientMemberIdValid = computed(() => {
  return patientMemberIdPattern.test(data.value.memberId);
});

const isMedicationValid = computed(() => {
  const value = searchFormData.value.medication;
  return value !== null && value.trim() !== "";
});

const isLastNameValid = computed(() => data.value.lastName.trim() !== "");

async function sendRequirements() {
  formButtonClicked.value = true;

  window.scrollTo({
    top: 100,
    behavior: "smooth",
  });

  if (
    isDobValid.value &&
    isCoverMyMedsKeyValid.value &&
    isLastNameValid.value &&
    isPatientMemberIdValid.value &&
    isMedicationValid.value
  ) {
    try {
      showPreloader.value = true;

      const service = route.name === "request-missing-requirements" ? mainServices : denialService;
      await service[route.name === "request-missing-requirements" ? "requestRequirements" : "requestDenialReport"](
        data.value
      );

      formButtonClicked.value = false;
      errors.value = [];
      clearTheForm();
      successModalWindow.value = true;
    } catch (err) {
      errors.value = tryParseApiErrors(err);
    }
    showPreloader.value = false;
  }
}

function clearTheForm() {
  data.value.coverMyMedsKey = "";
  data.value.lastName = "";
  data.value.dob = "";
  data.value.memberId = "";
  data.value.medication = "";
}
</script>

<style lang="scss" scoped>
@import "../styles/components/_request-form";
</style>
