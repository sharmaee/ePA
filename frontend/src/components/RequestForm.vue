<template>
  <div class="form">
    <div class="row-with-two-input">
      <div class="cover-my-meds-key">
        <label for="cover-my-meds-key">CoverMyMeds Key</label>
        <input id="cover-my-meds-key" v-model="data.coverMyMedsKey" type="text" placeholder="eg. B4HL4T2E" />
        <span v-if="!isCoverMyMedsKeyValid && formButtonClicked" class="input-error-notification">
          Please enter a valid CoverMyMeds Key.
        </span>
      </div>
      <div class="patient-last-name">
        <label for="patient-last-name">Patient Last Name</label>
        <input id="patient-last-name" v-model="data.lastName" type="text" placeholder="eg. Snow" />
        <span v-if="!isLastNameValid && formButtonClicked" class="input-error-notification">
          Please enter ALL fields to search.
        </span>
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
        <span v-if="!isPatientMemberIdValid && formButtonClicked" class="input-error-notification">
          Please add the correct email
        </span>
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
      By clicking the button below, I authorize service providers acting on behalf of Quantification by Design Inc. dba
      Lamar Health (“Lamar Health”) to obtain, use, share, disclose, and store the patient's personal and medical
      information to provide access support (“Support”). I understand that such Support may require contact with:
      applicable health insurer(s); and any pharmacy involved in my (or the patient's) treatment. I understand that I do
      not need to sign this form in order to obtain treatment, insurance, or insurance benefits; I am required to sign
      it only if I wish to receive optional Lamar Health support. I understand I can revoke my authorization at any time
      by emailing my revocation to
      <a href="mailto:security@lamarhealth.com">security@lamarhealth.com</a>.
    </span>
    <button @click="sendRequirements">{{ btnText }}</button>
    <br />
    <span v-if="errMessage" class="input-error-notification"
      >Sorry, something went wrong. Please contact us at <a href="mailto:dev@lamarhealth.com">dev@lamarhealth.com</a> or
      try again later</span
    >
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { mainServices } from "@/services/mainServices";
import { denialService } from "@/services/denialService";
import { storeToRefs } from "pinia";
import { useSearchFormStore } from "@/stores/searchFormStore";
import { useUiElementsStore } from "@/stores/uiElementsStore";
import { useRoute } from "vue-router";
const { searchFormData } = storeToRefs(useSearchFormStore());

const route = useRoute();

const { showPreloader, successModalWindow } = storeToRefs(useUiElementsStore());
const btnText = route.name === "request-without-requirements" ? "Email me steps" : "Submit";

const formButtonClicked = ref(false);
const errMessage = ref(false);

const data = ref({
  medication: searchFormData.value.medication,
  insuranceProvider: searchFormData.value.insuranceProvider,
  insuranceCoverageState: searchFormData.value.insuranceCoverageState,
  coverMyMedsKey: "",
  lastName: "",
  dob: "",
  memberId: "",
  maEmail: "",
  releaseVersion: "0.0.1",
});

// Validators
const isEmailValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(data.value.maEmail);
});

const isDobValid = computed(() => {
  const dobPattern = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$/;
  return dobPattern.test(data.value.dob);
});

const isCoverMyMedsKeyValid = computed(() => {
  const coverMyMedsKeyPattern = /^[A-Za-z0-9]{6,8}$/;
  return coverMyMedsKeyPattern.test(data.value.coverMyMedsKey);
});

const isLastNameValid = computed(() => data.value.lastName.trim() !== "");
const isPatientMemberIdValid = computed(() => data.value.memberId.trim() !== "");

async function sendRequirements() {
  formButtonClicked.value = true;

  window.scrollTo({
    top: 100,
    behavior: "smooth",
  });

  if (
    isEmailValid.value &&
    isDobValid.value &&
    isCoverMyMedsKeyValid.value &&
    isLastNameValid.value &&
    isPatientMemberIdValid.value
  ) {
    try {
      showPreloader.value = true;

      const service = route.name === "request-without-requirements" ? mainServices : denialService;
      await service[route.name === "request-without-requirements" ? "requestRequirements" : "requestDenialReport"](
        data.value
      );

      formButtonClicked.value = false;
      clearTheForm();
    } catch (err) {
      clearTheForm();
      errMessage.value = err;
    }
    showPreloader.value = false;
    successModalWindow.value = true;
  }
}

function clearTheForm() {
  data.value.coverMyMedsKey = "";
  data.value.lastName = "";
  data.value.dob = "";
  data.value.memberId = "";
  data.value.maEmail = "";
}
</script>

<style lang="sass" scoped>
@import "../styles/components/_request-form"
</style>
