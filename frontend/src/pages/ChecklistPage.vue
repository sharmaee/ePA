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

      <div v-for="(section, index) in smartEngineCheckboxContent" :key="index" class="smart-engine-list">
        <span class="smart-engine-list-header">{{ section.header }}</span>
        <span v-for="(item, itemIndex) in section.items" :key="itemIndex" class="check-item">
          <input :id="`item-${index}-${itemIndex}`" type="checkbox" />
          <label :for="`item-${index}-${itemIndex}`">{{ item }}</label>
        </span>
      </div>
      <div class="additional-info">
        <p>
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

      <table>
        <thead>
          <tr>
            <th>
              <div class="square">
                <div class="check-box-square"></div>
              </div>
            </th>
            <th>ICD-10 Codes</th>
            <th>Diagnosis</th>
            <th>Lab Results to Attach</th>
            <th>Supporting documents</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in smartEngineTable" :key="item.diagnosis">
            <td>
              <div class="table-input-wrapper">
                <input type="checkbox" />
              </div>
            </td>
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
import { ref } from "vue";
import ChecklistRecursiveComponent from "@/pages/ChecklistRecursiveComponent";
import smartEngineTable from "@/json-data/smart-engine-table";
import smartEngineCheckboxContent from "@/json-data/smart-engine-checkbox-content";

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
