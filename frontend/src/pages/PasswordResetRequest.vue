<template>
  <PriorHeader />

  <div class="forgot-form-wrapper">
    <h1 class="registration-page-title">Forgot Password</h1>
    <p class="forgot-pass-sub-title">Forgot your password? No problem!</p>
    <ModalWindowForSuccessRequest
      v-if="successModalWindow"
      :modal-content="modalContent"
      @close-modal-window="closeSuccessModalWindow" />
    <div v-else class="form">
      <p>Enter your registered email address below, and we'll send you a link to reset your password</p>
      <div class="your-email">
        <input id="your-email" v-model="userEmail" type="text" placeholder="example@findsunrise.com" />
        <span v-if="!isEmailValid && formButtonClicked" class="input-error-notification">
          Please enter a valid email address.
        </span>
      </div>
      <button @click="passwordSending">Get Password Reset Link</button>
    </div>
  </div>

  <PriorFooter />
</template>

<script setup>
import { ref, computed } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import authService from "@/services/authService";

import ModalWindowForSuccessRequest from "@/components/ModalWindowForSuccessRequest";

const successModalWindow = ref(false);

const modalContent = {
  header: "",
  content: "Check your email, and click the link there",
};

const userEmail = ref("");
const errors = ref([]);
const formButtonClicked = ref(false);

// Validators
const isEmailValid = true;
// const isEmailValid = computed(() => {
//   const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   const email = userEmail.value;
//   return email !== "" && emailPattern.test(email);
// });

const passwordSending = async () => {
  formButtonClicked.value = true;
  // if (isEmailValid.value) {
  try {
    await authService.passwordResetRequest(userEmail.value);
    formButtonClicked.value = false;
    successModalWindow.value = true;
  } catch (error) {
    console.log(errors.value);
    successModalWindow.value = true;
  }
  // }
};

function closeSuccessModalWindow() {
  successModalWindow.value = false;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
