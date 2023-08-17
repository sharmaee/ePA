<template>
  <div class="success-request-modal-window">
    <div class="cross-wrapper">
      <img src="@/assets/images/cross-for-the-close.svg" alt="cross" @click="closeModalWindow" />
    </div>
    <div class="modal-content-wrapper">
      <div class="main-window-img-wrapper">
        <img :src="props.modalImg" alt="modal-img" />
      </div>
      <span class="modal-header">{{ props.modalContent.header }}</span>
      <span class="model-content">{{ props.modalContent.content }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modalImg: {
    type: String,
    default: require("@/assets/images/modal-green-checkmark.svg"),
  },
  modalContent: {
    type: Object,
    required: true,
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
