<template>
  <div class="smart-engine-wrapper">
    <h3>Follow these steps to increase the chance of approval:</h3>

    <div v-for="(section, index) in smartEngineCheckList" :key="index" class="smart-engine-list">
      <span class="smart-engine-list-header">Step {{ index + 1 }}: {{ section.header }}</span>
      <span v-for="(item, itemIndex) in section.items" :key="itemIndex" class="check-item">
        <input :id="`item-${index}-${itemIndex}`" v-model="item.checked" type="checkbox" />
        <label :for="`item-${index}-${itemIndex}`">{{ item.label }}</label>
        <span v-if="submitClicked && !item.checked" class="error-message">
          {{ item.validation }}
        </span>
      </span>
      <div v-if="section.additional_info" class="additional-info-wrapper">
        {{ section.additional_info }}
      </div>
      <button v-if="section.additional_info" @click="copyAdditionalInfoToClipboard(section.additional_info)">
        {{ copyAdditionalInfoButtonText }}
      </button>
    </div>

    <div class="smart-engine-table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Diagnosis</th>
            <th>ICD-10 Codes</th>
            <th>Clinical Study Documents</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredByDiagnosisData" :key="item.diagnosis">
            <td>{{ item.diagnosis }}</td>
            <td>{{ item.icd_10_codes.join(", ") }}</td>
            <td>
              <div class="download">
                <a :href="item.supporting_documents" target="_blank">Download</a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="form">
      <div class="row-with-one-input">
        <div class="cover-my-meds-key">
          <label for="cover-my-meds-key">CoverMyMeds Key</label>
          <input
            id="cover-my-meds-key"
            v-model="data.coverMyMedsKey"
            type="text"
            placeholder="B4HL4T2E"
            @keyup="(event) => sendFormByEnterClicking(event, validateCheckList)" />
          <span v-if="!isCoverMyMedsKeyValid && submitClicked" class="input-error-notification">
            Please enter a valid CoverMyMeds Key.
          </span>
        </div>
      </div>
    </div>
    <div class="smart-engine-submit">
      <button class="smart" @click="validateCheckList">Complete</button>
    </div>
    <span v-if="errors.length > 0" class="input-error-notification">
      <span v-for="error in errors" :key="error">{{ error }}</span>
      Sorry, something went wrong. Please contact us at
      <a href="mailto:founders@lamarhealth.com"> founders@lamarhealth.com</a> or try again later
    </span>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { tryParseApiErrors, sendFormByEnterClicking } from "@/utils";
import { mainServices } from "@/services/mainServices";

import smartEngineTable from "@/json-data/smart-engine-table";
import smartEngineCheckboxContent from "@/json-data/smart-engine-checkbox-content";

const submitClicked = ref(false);
const copyAdditionalInfoButtonText = ref("Copy Paragraph");

const props = defineProps({
  diagnosisFilterData: {
    type: Object,
    required: true,
  },
  stepVerifyDocs: {
    type: Object,
    required: true,
  },
  smartEngineKeyData: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["show-success-engine-page"]);

const filteredByDiagnosisData = computed(() => {
  return smartEngineTable.filter((element) => props.diagnosisFilterData.includes(element.diagnosis));
});

const data = ref({
  coverMyMedsKey: "",
});

const coverMyMedsKeyPattern = /^[A-Za-z0-9]{6,8}$/;

const isCoverMyMedsKeyValid = computed(() => {
  return coverMyMedsKeyPattern.test(data.value.coverMyMedsKey);
});

const errors = ref([]);

const staticCheckboxContent = ref([]);
staticCheckboxContent.value = [...smartEngineCheckboxContent];

const smartEngineCheckList = computed(() => {
  const smartEngineCheckList = staticCheckboxContent.value;
  smartEngineCheckList.splice(2, 0, props.stepVerifyDocs[props.smartEngineKeyData]);
  if (props.diagnosisFilterData.includes("Type 2 diabetes (DM)")) {
    smartEngineCheckList.shift();
  } else {
    smartEngineCheckList.splice(1, 1);
  }
  smartEngineCheckList.forEach((section) => {
    section.items.forEach((item) => {
      item.checked = false;
    });
  });
  return smartEngineCheckList;
});

function copyAdditionalInfoToClipboard(content) {
  copyAdditionalInfoButtonText.value = "Copied!";
  try {
    navigator.clipboard.writeText(content);
  } catch (error) {
    copyAdditionalInfoButtonText.value = "Copy Paragraph";
  }
  setTimeout(() => (copyAdditionalInfoButtonText.value = "Copy Paragraph"), 3000);
}

function validateCheckList() {
  submitClicked.value = true;
  if (isCoverMyMedsKeyValid.value) {
    sendPriorAuthorization();
    if (smartEngineCheckList.value.every((section) => section.items.every((item) => item.checked))) {
      emit("show-success-engine-page");
    } else {
      const firstFailedValidation = smartEngineCheckList.value.find((section) =>
        section.items.find((item) => !item.checked)
      );
      const firstFailedValidationIndex = smartEngineCheckList.value.indexOf(firstFailedValidation);
      const firstFailedValidationItemIndex = firstFailedValidation.items.findIndex((item) => !item.checked);
      const firstFailedValidationItemId = `item-${firstFailedValidationIndex}-${firstFailedValidationItemIndex}`;
      const firstFailedValidationItem = document.getElementById(firstFailedValidationItemId);
      firstFailedValidationItem.scrollIntoView({ behavior: "smooth" });
    }
  }
}

async function sendPriorAuthorization() {
  try {
    await mainServices.submitPriorAuthorization(data.value);
    errors.value = [];
  } catch (err) {
    // errors.value = tryParseApiErrors(err);
    console.log(err);
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_smart-engine-container.scss";
</style>
