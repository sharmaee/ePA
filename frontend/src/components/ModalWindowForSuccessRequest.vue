<template>
  <div class="success-request-modal-window">
    <div class="cross-wrapper">
      <img @click="closeModalWindow" src="@/assets/images/cross-for-the-close.svg" alt="cross" />
    </div>
    <div class="modal-content-wrapper">
      <div class="main-window-img-wrapper">
        <img :src="props.modalWindow.img" alt="modal-img" />
      </div>
      <span class="modal-header">{{ props.modalWindow.header }}</span>
      <span class="model-content">{{ props.modalWindow.content }}</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  modalWindow: {
    type: Object,
    required: true,
    default: () => ({
      img: require("@/assets/images/modal-green-checkmark.svg"),
      header: "Submission Received!",
      content: "Our team is on it. Expect instructions within 24 hours.",
    }),
  },
});

const emit = defineEmits(["close-modal-window"]);

function closeModalWindow() {
  emit("close-modal-window");
}
</script>

<style lang="scss" scoped>
@import "../styles/components/_modal-window-for-success-request.scss";
</style>
