<template>
  <PriorHeader />
  <div class="missing-requirements-wrapper">
    <h1 :class="{ hide: screenWidth < 835 }">Denial Report</h1>
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <div v-if="showPreloader" class="preloader-wrapper">
      <GreenCirclePreloader />
    </div>
    <ModalWindowForSuccessRequest
      v-if="successModalWindow"
      :modal-content="modalContent"
      @close-modal-window="closeSuccessModalWindow" />

    <div class="request-missing-requirements-form-wrapper">
      <div v-if="!showPreloader && !successModalWindow" class="missing-requirements-form">
        <h2>Get updated criteria for improving first time approval rates.</h2>
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
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import ModalWindowForSuccessRequest from "@/components/ModalWindowForSuccessRequest";
import { storeToRefs } from "pinia";

import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import RequestForm from "@/components/RequestForm";

import { useUiElementsStore } from "@/stores/uiElementsStore";

const { showPreloader, successModalWindow } = storeToRefs(useUiElementsStore());

const screenWidth = ref(null);

const modalContent = {
  header: "",
  content: `You will get an email with the best medication to provide as an alternative 
            and help prevent the denial from happening next time. You are helping yourself 
            and medical assistants everywhere fight denials.`,
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
@import "../styles/pages/_request-denial-report";
</style>
