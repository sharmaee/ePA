import { defineStore } from "pinia";
import { ref } from "vue";

export const useCheckListStore = defineStore("check-list-child", () => {
  const checkListChild = ref({});

  return {
    checkListChild,
  };
});
