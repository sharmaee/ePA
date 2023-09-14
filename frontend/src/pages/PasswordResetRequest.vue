<template>
  <PriorHeader />
  <div class="forgot-form-wrapper">
    <h1 class="registration-page-title">Reset Password</h1>
    <GreenCirclePreloader v-if="showPreloader" />
    <div v-else-if="!showPreloader && passwordRequestEmailSent" class="final-registered-notification">
      <div class="form">
        <div class="envelop-wrapper">
          <img src="@/assets/images/envelop.svg" alt="envelop" />
        </div>
        <p>Check your email, you will receive a link to reset your password.</p>
      </div>
    </div>
    <div v-else-if="!showPreloader && !passwordRequestEmailSent">
      <p class="forgot-pass-sub-title">Forgot your password? No problem!</p>
      <div class="form">
        <p>Enter your registered email address below, and we'll send you a link to reset your password</p>
        <div class="your-email">
          <input id="your-email" v-model="userEmail" type="text" placeholder="example@findsunrise.com" />
          <span v-if="!isEmailValid && formButtonClicked" class="input-error-notification">
            Please enter a valid email address.
          </span>
        </div>
        <button @click="passwordSending">Get Password Reset Link</button>
        <span v-if="errors.length > 0" class="input-error-notification">
          <span v-for="error in errors" :key="error">{{ error }}</span>
        </span>
      </div>
    </div>
  </div>

  <PriorFooter />
</template>

<script setup>
import { ref, computed } from "vue";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import authService from "@/services/authService";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import { tryParseApiErrors } from "@/utils";

const errors = ref([]);
const showPreloader = ref(false);
const passwordRequestEmailSent = ref(false);

const userEmail = ref("");
const formButtonClicked = ref(false);

// Validators
const isEmailValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const email = userEmail.value;
  return email !== "" && emailPattern.test(email);
});

const passwordSending = async () => {
  formButtonClicked.value = true;

  if (isEmailValid.value) {
    showPreloader.value = true;
    try {
      await authService.passwordResetRequest(userEmail.value);
      formButtonClicked.value = false;
      showPreloader.value = false;
      passwordRequestEmailSent.value = true;
      userEmail.value = "";
      errors.value = [];
    } catch (error) {
      errors.value = tryParseApiErrors(error);
    }
  }
  showPreloader.value = false;
};
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
