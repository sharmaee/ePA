import { defineStore } from "pinia";
import { shallowRef } from "vue";

export const useFlowRequirements = defineStore("flow-requirements", () => {
  const flowRequirements = shallowRef(null);

  return { flowRequirements };
});
