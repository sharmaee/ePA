<template>
  <PriorHeader />
  <div class="missing-requirements-wrapper">
    <h1 :class="{ hide: screenWidth < 835 }">Request Call For Criteria</h1>
    <p>Our Agents Are On Stand-By To Find What You Need To Submit.<br />Current expected Turnaround: &lt; 24 hours</p>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div v-if="showPreloader" class="preloader-wrapper">
      <GreenCirclePreloader />
    </div>
    <ModalWindowForSuccessRequestVue
      v-if="successModalWindow"
      :modal-content="modalContent"
      @close-modal-window="closeSuccessModalWindow" />

    <div class="request-missing-requirements-form-wrapper">
      <div v-if="!showPreloader && !successModalWindow" class="missing-requirements-form">
        <h2>Get the exact preparation steps your patient needs.</h2>
        <hr />
        <RequestForm />
      </div>
    </div>
    <div class="shadow-ellipse shadow-ellipse-left"></div>
  </div>

  <PriorFooter />
</template>

<script setup>
import { ref } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import { storeToRefs } from "pinia";
import ModalWindowForSuccessRequestVue from "@/components/ModalWindowForSuccessRequest";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import RequestForm from "@/components/RequestForm";
import { useUiElementsStore } from "@/stores/uiElementsStore";

const { showPreloader, successModalWindow } = storeToRefs(useUiElementsStore());

const screenWidth = ref(null);

const modalContent = {
  header: "Submission Received!",
  content: "Our team is on it. Expect instructions within 24 hours.",
};

function displayWindowSize() {
  screenWidth.value = document.documentElement.clientWidth;
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();

function closeSuccessModalWindow() {
  successModalWindow.value = false;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_request-missing-requirements";
</style>
