import { defineStore } from "pinia";
import { ref } from "vue";

export const useMainFormStore = defineStore("main-form-data", () => {
  const searchFormData = ref({
    insuranceProvider: null,
    insuranceCoverageState: null,
    medication: "Wegovy",
  });

  return {
    searchFormData,
  };
});
