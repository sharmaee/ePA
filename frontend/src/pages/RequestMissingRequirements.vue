<template>
  <PriorHeader />
  <div class="missing-requirements-wrapper">
    <h1 :class="{ hide: screenWidth < 835 }">Request Call For Criteria</h1>
    <p>Our Agents Are On Stand-By To Find What You Need To Submit.<br />Current expected Turnaround: &lt; 24 hours</p>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div class="request-missing-requirements-form-wrapper">
      <div class="missing-requirements-form">
        <h2>Get the exact preparation steps your patient needs.</h2>
        <hr />
        <div class="form">
          <div class="row-with-two-input">
            <div class="cover-my-meds-key">
              <label for="cover-my-meds-key">CoverMyMeds Key</label>
              <input id="cover-my-meds-key" v-model="data.coverMyMedsKey" type="text" placeholder="eg. B4HL4T2E" />
            </div>
            <div class="patient-last-name">
              <label for="patient-last-name">Patient Last Name</label>
              <input id="patient-last-name" v-model="data.lastName" type="text" placeholder="eg. Snow" />
            </div>
          </div>

          <div class="row-with-two-input">
            <div class="date-of-birth">
              <label for="date-of-birth">Date Of Birth</label>
              <input id="date-of-birth" v-model="data.dob" type="text" placeholder="eg. MM/DD/YYYY" />
              <span v-if="!isDobValid && formButtonClicked" class="input-error-notification">
                Please enter a valid date of birth (MM/DD/YYYY).
              </span>
            </div>
            <div class="patient-member-id">
              <label for="patient-member-id">Patient Member ID</label>
              <input id="patient-member-id" v-model="data.memberId" type="text" placeholder="eg. H3485045" />
            </div>
          </div>

          <div class="row-with-one-input">
            <div class="your-email">
              <label for="your-email">Your Email</label>
              <input id="your-email" v-model="data.maEmail" type="text" placeholder="example@findsunrise.com" />
              <span v-if="!isEmailValid && formButtonClicked" class="input-error-notification">
                Please add the correct email
              </span>
            </div>
          </div>
          <span class="agreement">
            By clicking the button below, I authorize service providers acting on behalf of Quantification by Design
            Inc. dba Lamar Health (“Lamar Health”) to obtain, use, share, disclose, and store the patient's personal and
            medical information to provide access support (“Support”). I understand that such Support may require
            contact with: applicable health insurer(s); and any pharmacy involved in my (or the patient's) treatment. I
            understand that I do not need to sign this form in order to obtain treatment, insurance, or insurance
            benefits; I am required to sign it only if I wish to receive optional Lamar Health support. I understand I
            can revoke my authorization at any time by emailing my revocation to
            <a href="mailto:security@lamarhealth.com">security@lamarhealth.com</a>.
          </span>
          <button @click="sendRequirements">Email me steps</button>
        </div>
      </div>
    </div>
    <div class="shadow-ellipse shadow-ellipse-left"></div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { ref, computed } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import { mainServices } from "@/services/mainServices";

import { storeToRefs } from "pinia";
import { useMainFormStore } from "@/stores/mainFormStore";

const { searchFormData } = storeToRefs(useMainFormStore());

const screenWidth = ref(null);
const formButtonClicked = ref(null);

const data = ref({
  medication: searchFormData.medication,
  insuranceProvider: searchFormData.insuranceProvider,
  insuranceCoverageState: searchFormData.insuranceCoverageState,
  lastName: "",
  dob: "",
  memberId: "",
  maEmail: "",
  releaseVersion: "0.0.1",
});

function displayWindowSize() {
  screenWidth.value = document.documentElement.clientWidth;
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();

// Validators
const isEmailValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(data.value.maEmail);
});

const isDobValid = computed(() => {
  const dobPattern = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$/;
  return dobPattern.test(data.value.dob);
});

async function sendRequirements() {
  formButtonClicked.value = true;

  if (isEmailValid.value && isDobValid.value) {
    try {
      await mainServices.requestRequirements(data.value);

      formButtonClicked.value = false;
    } catch (error) {
      console.log(error);
    }
  }
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_request-missing-requirements"
</style>
