<template>
  <PriorHeader />
  <div v-if="!showResetPasswordForm" class="forgot-form-wrapper">
    <h1 class="registration-page-title">Forgot Password</h1>
    <p>Forgot your password? No problem!</p>
    <div class="form">
      <p>Enter your registered email address below, and we'll send you a link to reset your password</p>
      <div class="your-email">
        <label for="your-email">Email Address</label>
        <input id="your-email" v-model="userEmail" type="text" placeholder="example@findsunrise.com" />
        <span v-if="!isEmailValid && formButtonClicked" class="input-error-notification">
          Please enter a valid email address.
        </span>
      </div>
      <button @click="showRestPasswordForm">Get Password Reset Link</button>
    </div>
  </div>

  <div v-else class="reset-form-wrapper">
    <h1 class="registration-page-title">Reset Password</h1>
    <div class="form">
      <p>To complete the password reset process, please enter your new password below and confirm.</p>
      <div class="password">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" />
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
      <button @click="resetPassword">Reset Password</button>
    </div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { ref, computed } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import authService from "@/services/authService";

const formButtonClicked = ref(false);
const showResetPasswordForm = ref(false);

const userEmail = ref("");
const password = ref("");
const passwordConfirmation = ref("");

// Validators
const isEmailValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const email = userEmail.value;
  return email !== "" && emailPattern.test(email);
});

const isPasswordValid = computed(() => {
  const password = password.value;
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{11,}$/;

  return passwordPattern.test(password);
});

const isPasswordMatchValid = computed(() => {
  return password.value === passwordConfirmation.value;
});

async function showRestPasswordForm() {
  formButtonClicked.value = true;

  if (isEmailValid.value) {
    formButtonClicked.value = false;
    showResetPasswordForm.value = true;
  }
}

async function resetPassword() {
  formButtonClicked.value = true;

  if (isPasswordValid.value && isPasswordMatchValid.value) {
    console.log();
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
