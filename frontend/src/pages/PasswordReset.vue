<template>
  <PriorHeader />
  <div class="reset-form-wrapper">
    <h1 v-if="!passwordUpdated" class="registration-page-title">Reset Password</h1>
    <GreenCirclePreloader v-if="showPreloader" />
    <div v-else-if="!showPreloader && passwordUpdated">
      <h1 class="registration-page-title">Password Changed</h1>
      <div class="final-registered-notification">
        <div class="form">
          <p>Password changed successfully!</p>
          <button @click="redirectionToLoginPage">Continue To Login</button>
        </div>
      </div>
    </div>
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
import { useRoute, useRouter } from "vue-router";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import { tryParseApiErrors } from "@/utils";

const errors = ref([]);
const showPreloader = ref(false);
const route = useRoute();
const router = useRouter();

const formButtonClicked = ref(false);
const passwordUpdatedCorrectly = ref(false);
const passwordUpdated = ref(false);

const newPassword = ref("");
const passwordConfirmation = ref("");

// Validators
const isPasswordValid = computed(() => {
  const password = newPassword.value;
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{11,}$/;

  return passwordPattern.test(password);
});

const isPasswordMatchValid = computed(() => {
  return newPassword.value === passwordConfirmation.value;
});

const updatePassword = async () => {
  formButtonClicked.value = true;

  if (isPasswordValid.value && isPasswordMatchValid.value) {
    showPreloader.value = true;
    try {
      await authService.passwordReset(newPassword.value, route.params.token);
      passwordUpdatedCorrectly.value = true;
      showPreloader.value = false;
      newPassword.value = "";
      passwordConfirmation.value = "";
      passwordUpdated.value = true;
      errors.value = [];
    } catch (error) {
      errors.value = tryParseApiErrors(error);
    }
  }
  showPreloader.value = false;
};

function redirectionToLoginPage() {
  router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
