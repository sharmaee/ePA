<template>
  <div class="smart-engine-wrapper">
    <h3>Follow these steps to increase the chance of approval:</h3>

    <div v-for="(section, index) in smartEngineCheckList" :key="index" class="smart-engine-list">
      <span class="smart-engine-list-header">{{ section.header }}</span>
      <span v-for="(item, itemIndex) in section.items" :key="itemIndex" class="check-item">
        <input :id="`item-${index}-${itemIndex}`" type="checkbox" />
        <label :for="`item-${index}-${itemIndex}`">{{ item }}</label>
      </span>
      <div v-if="section.additional_info" class="additional-info-wrapper">
        <md-block class="additional-info">
          {{ section.additional_info }}
        </md-block>
      </div>
      <button v-if="section.additional_info" @click="copyAdditionalInfoToClipboard(section.additional_info)">
        {{ copyAdditionalInfoButtonText }}
      </button>
    </div>

    <div class="smart-engine-table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ICD-10 Codes</th>
            <th>Diagnosis</th>
            <th>Lab Results to Attach</th>
            <th>Supporting documents</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredByComorbidityData" :key="item.diagnosis">
            <td>{{ item.icd_10_codes.join(", ") }}</td>
            <td>{{ item.diagnosis }}</td>
            <td>{{ item.lab_results_to_attach.join(", ") }}</td>
            <td>
              <div class="download">
                <a :href="item.supporting_documents" target="_blank">Download</a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import smartEngineTable from "@/json-data/smart-engine-table";
import smartEngineCheckboxContent from "@/json-data/smart-engine-checkbox-content";
const copyAdditionalInfoButtonText = ref("Copy Paragraph");
const props = defineProps({
  comorbidityFilterData: {
    type: Object,
    required: true,
  },
  stepVerifyDocs: {
    type: Object,
    required: true,
  },
});

const filteredByComorbidityData = computed(() => {
  return smartEngineTable.filter((element) => props.comorbidityFilterData.includes(element.diagnosis));
});

const smartEngineCheckList = computed(() => {
  const smartEngineCheckList = [...smartEngineCheckboxContent];
  smartEngineCheckList.splice(1, 0, props.stepVerifyDocs);
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
</script>

<style lang="scss" scoped>
@import "../styles/pages/_smart-engine-container.scss";
</style>
