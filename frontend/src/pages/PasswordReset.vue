<template>
  <PriorHeader />
  <div class="reset-form-wrapper">
    <h1 class="registration-page-title">Reset Password</h1>
    <ModalWindowForSuccessRequest
      v-if="successModalWindow"
      :modal-content="modalContent"
      @close-modal-window="closeSuccessModalWindow" />
    <div v-else class="form">
      <p>To complete the password reset process, please enter your new password below and confirm.</p>
      <div class="password">
        <label for="password">Password</label>
        <input id="password" v-model="newPassword" type="password" />
        <span v-if="!isPasswordValid && formButtonClicked" class="input-error-notification">
          Please create a password with more than 10 characters, at least 1 uppercase and 1 lowercase letter, 1 number,
          and 1 symbol.
        </span>
      </div>
      <div class="confirm-password">
        <label for="confirm-password">Confirm Password</label>
        <input id="confirm-password" v-model="passwordConfirmation" type="password" />
        <span v-if="!isPasswordMatchValid && formButtonClicked" class="input-error-notification">
          Passwords must match.
        </span>
      </div>
      <button @click="updatePassword">Reset Password</button>
    </div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { ref, computed } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import authService from "@/services/authService";
import { useRoute } from "vue-router";

import ModalWindowForSuccessRequest from "@/components/ModalWindowForSuccessRequest";

const route = useRoute();

const formButtonClicked = ref(false);
const successModalWindow = ref(false);

const newPassword = ref("");
const passwordConfirmation = ref("");

const modalContent = {
  header: "",
  content: "Password changed",
};

// Validators
const isPasswordValid = computed(() => {
  const password = newPassword.value;
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{11,}$/;

  return passwordPattern.test(password);
});

const isPasswordMatchValid = computed(() => {
  return newPassword.value === passwordConfirmation.value;
});

console.log(route.params);

const updatePassword = async () => {
  if (isPasswordValid.value && isPasswordMatchValid.value) {
    try {
      await authService.passwordReset(newPassword.value, route.params.token);
      successModalWindow.value = true;
    } catch (error) {
      console.log(error);
    }
  }
};

function closeSuccessModalWindow() {
  successModalWindow.value = false;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
