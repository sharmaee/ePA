<template>
  <div v-if="!showFinalWindow" class="smart-engine-wrapper">
    <h3>Follow these steps to increase the chance of approval:</h3>

    <div v-for="(section, index) in smartEngineCheckList" :key="index" class="smart-engine-list">
      <span class="smart-engine-list-header">Step {{ index + 1 }}: {{ section.header }}</span>
      <span v-for="(item, itemIndex) in section.items" :key="itemIndex" class="check-item">
        <input :id="`item-${index}-${itemIndex}`" v-model="item.checked" type="checkbox" />
        <label :for="`item-${index}-${itemIndex}`">{{ item.label }}</label>
        <span v-if="submitClicked && !item.checked" class="error-message">Please, check the item</span>
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
    <div class="smart-engine-submit">
      <button class="smart" @click="checkCheckboxes">Submit</button>
    </div>
    <!-- <div class="smart-engine-start-new-patient">
      <span @click="redirectToHomePage">Start New Patient >></span>
    </div> -->
  </div>
  <div v-else class="smart-engine-success-wrapper">
    <div class="smart-engine-success-img">
      <img src="@/assets/images/modal-green-checkmark.svg" alt="success" />
    </div>
    <h2>Complete!</h2>
    <p>Thanks to your efforts, our patients are one step closer to achieving their health goals.</p>
    <div class="smart-engine-start-new-patient">
      <button @click="redirectToHomePage">Start New Patient</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import smartEngineTable from "@/json-data/smart-engine-table";
import smartEngineCheckboxContent from "@/json-data/smart-engine-checkbox-content";
import { useRouter } from "vue-router";

const submitClicked = ref(false);
const allCheckboxesFilled = ref(true);
const showFinalWindow = ref(false);
const router = useRouter();
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

const emit = defineEmits(["hide-requirements-page-header"]);

const filteredByDiagnosisData = computed(() => {
  return smartEngineTable.filter((element) => props.diagnosisFilterData.includes(element.diagnosis));
});

const smartEngineCheckList = computed(() => {
  const smartEngineCheckList = [...smartEngineCheckboxContent];
  smartEngineCheckList.splice(1, 0, props.stepVerifyDocs[props.smartEngineKeyData]);
  if (props.diagnosisFilterData.includes("Type 2 diabetes (DM)")) {
    smartEngineCheckList.shift();
  }
  return smartEngineCheckList;
});

function copyAdditionalInfoToClipboard(content) {
  copyAdditionalInfoButtonText.value = "Copied!";

  try {
    navigator.clipboard.writeText(content);
  } catch (error) {
    copyAdditionalInfoButtonText.value = "Copy Paragraph";
  }
}

function redirectToHomePage() {
  router.push({ name: "home-page" });
}

function checkCheckboxes() {
  submitClicked.value = true;

  for (const section of smartEngineCheckList.value) {
    for (const item of section.items) {
      if (!item.checked) {
        allCheckboxesFilled.value = false;
      }
    }
  }

  if (allCheckboxesFilled.value) {
    emit("hide-requirements-page-header");
    sendData();
    showFinalWindow.value = true;
  }
}

async function sendData() {
  console.log("hey");
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_smart-engine-container.scss";
.error-message {
  color: red;
  font-size: 14px;
}
</style>
