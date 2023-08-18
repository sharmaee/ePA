import { defineStore } from "pinia";
import { ref } from "vue";

export const useSearchFormStore = defineStore("search-form-data", () => {
  const searchFormData = ref({
    insuranceProvider: null,
    insuranceCoverageState: null,
    medication: "Wegovy (semaglutide)",
  });

  return {
    searchFormData,
  };
});
