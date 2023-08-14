<template>
  <div class="checklist-wrapper">
    <div v-if="props.data && props.data.children">
      <div v-for="option in props.data.children" :key="option.label">
        <ChecklistRecursiveComponent :data="option" />
      </div>
    </div>
    <button @click="showSmartEngineContent">Submit</button>

    <div v-if="smartEngine" class="smart-engine-wrapper">
      <h3>Follow these steps to increase the chance of approval:</h3>
      <div class="smart-engine-list">
        <span class="smart-engine-list-header"
          >Step 1: Search and attach any of the following as evidence supporting pre-diabetes.
        </span>
        <span class="check-item">
          <input id="icd-10" type="checkbox" />
          <label for="icd-10">check if the patient has an ICD-10 code for R73.03</label>
        </span>
        <span class="check-item">
          <input id="pre-diabets" type="checkbox" />
          <label for="pre-diabets">Check if the doctor has mentioned pre-diabetes in the patient’s chart</label>
        </span>
        <span class="check-item">
          <input id="a1c" type="checkbox" />
          <label for="a1c">Check if the patient has A1C lab result of 5.7% or Higher</label>
        </span>
        <span class="check-item">
          <input id="fasting-glucose" type="checkbox" />
          <label for="fasting-glucose">check if the patient has fasting glucose levels of 100mg/dL or higher</label>
        </span>
      </div>
      <div class="smart-engine-list">
        <span class="smart-engine-list-header"
          >Step 1: Search and attach any of the following as evidence supporting pre-diabetes.
        </span>
        <span class="check-item">
          <input id="with-supporting-document" type="checkbox" />
          <label for="with-supporting-document">For each code found attach the supporting documents provided</label>
        </span>
        <span class="check-item">
          <input id="with-lab-result" type="checkbox" />
          <label for="with-lab-result"
            >for each code found check and attach the lab results suggested in the table</label
          >
        </span>
        <span class="check-item">
          <input id="medical-necessity" type="checkbox" />
          <label for="medical-necessity"
            >Edit this sentence to have ALL of the patients diagnosis and Request that a provider add it to the patients
            chart or in a letter of medical necessity.
          </label>
        </span>
        <p class="additional-info">
          “On examination, the patient's symptoms at their most severe, included
          <b>[insert symptoms from patients chart]</b>, abnormal lab results including
          <b>[list the lab results consistent with the diagnosis]</b>, and causing marked difficulty in performing daily
          activities. It is of vital importance to underline that the patient's condition has reached a critical stage
          where immediate intervention is no longer optional but a necessity. Failure to prescribe the indicated
          medication and initiate comprehensive care will likely lead to catastrophic consequences for the patient's
          health. This assessment is in accordance with clinical guidelines and best practice standards, as evidenced by
          the documents and research studies that my assistant will attach to this note. Should appropriate care not be
          initiated promptly, the patient is at imminent risk for serious complications such as heart attack, stroke,
          renal failure, severe infection, loss of limb due to peripheral arterial disease, and other life-threatening
          conditions. The urgency of this matter cannot be overstated, and I strongly urge that the necessary steps be
          taken without delay to prevent further deterioration of the patient's health.”
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ChecklistRecursiveComponent from "@/pages/ChecklistRecursiveComponent";
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
const smartEngine = ref(false);

function showSmartEngineContent() {
  smartEngine.value = !smartEngine.value;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_questionnaire-page.scss";
</style>
