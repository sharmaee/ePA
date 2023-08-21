import { defineStore } from "pinia";
import { ref } from "vue";

export const useUiElementsStore = defineStore("ui-elements", () => {
  const showPreloader = ref(false);
  const successModalWindow = ref(false);

  return {
    showPreloader,
    successModalWindow,
  };
});
