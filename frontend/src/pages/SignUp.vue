<template>
  <PriorHeader />
  <div class="registered-form-wrapper">
    <h1 v-if="!registerEmailSent" class="registration-page-title">Create Your Account</h1>
    <GreenCirclePreloader v-if="showPreloader" />
    <div v-if="registerEmailSent">
      <h1 class="registration-page-title">We are on it!</h1>
      <div class="final-registered-notification">
        <div class="form">
          <div class="envelop-wrapper">
            <img src="@/assets/images/envelop.svg" alt="envelop" />
          </div>
          <p>Check your email to get started with your account</p>
        </div>
      </div>
    </div>
    <div v-else-if="!showPreloader && !registerEmailSent" class="registration-form form">
      <div class="first-name">
        <label for="first-name">First Name</label>
        <input id="first-name" v-model="userInfo.first_name" type="text" placeholder="John" />
        <span v-if="!isFirstNameValid && formButtonClicked" class="input-error-notification">
          Please enter your first name.
        </span>
      </div>
      <div class="last-name">
        <label for="last-name">Last Name</label>
        <input id="last-name" v-model="userInfo.last_name" type="text" placeholder="Snow" />
        <span v-if="!isLastNameValid && formButtonClicked" class="input-error-notification">
          Please enter your last name.
        </span>
      </div>
      <div class="your-email">
        <label for="your-email">Email Address</label>
        <input id="your-email" v-model="userInfo.email" type="text" placeholder="example@findsunrise.com" />
        <span v-if="!isEmailValid && formButtonClicked" class="input-error-notification">
          Please enter a valid email address.
        </span>
      </div>
      <div class="password">
        <label for="password">Password</label>
        <input id="password" v-model="userInfo.password" type="password" />
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
      <button @click="registerUser">Create Account</button>
      <span v-if="errors.length > 0" class="input-error-notification">
        <span v-for="error in errors" :key="error">{{ error[0] }}</span>
      </span>
      <div class="auxiliary-account-links">
        <span class="have-an-account">
          Already have an account ?
          <router-link :to="{ name: 'login' }">Login</router-link>
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
import GreenCirclePreloader from "@/components/GreenCirclePreloader";
import authService from "@/services/authService";
import { tryParseApiErrors } from "@/utils";

const userInfo = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
});

const formButtonClicked = ref(false);
const errors = ref([]);
const showPreloader = ref(false);
const registerEmailSent = ref(false);
const passwordConfirmation = ref(null);

// Validators
const isFirstNameValid = computed(() => userInfo.value.first_name.trim() !== "");
const isLastNameValid = computed(() => userInfo.value.last_name.trim() !== "");

const isEmailValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const email = userInfo.value.email;
  return email !== "" && emailPattern.test(email);
});

const isPasswordValid = computed(() => {
  const password = userInfo.value.password;
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{11,}$/;

  return passwordPattern.test(password);
});

const isPasswordMatchValid = computed(() => {
  return userInfo.value.password === passwordConfirmation.value;
});

async function registerUser() {
  formButtonClicked.value = true;

  if (
    isFirstNameValid.value &&
    isLastNameValid.value &&
    isEmailValid.value &&
    isPasswordValid.value &&
    isPasswordMatchValid.value
  ) {
    try {
      showPreloader.value = true;
      await authService.register(userInfo.value);
      registerEmailSent.value = true;
      errors.value = [];
    } catch (error) {
      errors.value = tryParseApiErrors(error);
    }
  }
  showPreloader.value = false;
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
