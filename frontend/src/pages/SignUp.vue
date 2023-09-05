<template>
  <PriorHeader />
  <div class="registered-form-wrapper">
    <h1 class="registration-page-title">Create Your Account</h1>
    <div class="registration-form form">
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

      <div class="auxiliary-account-links">
        <router-link :to="{ name: 'home-page' }" class="forgot-pass-link">Forgot Password ?</router-link>
        <span class="have-an-account">
          Dont have an account ?
          <router-link :to="{ name: 'register' }">Create an account</router-link>
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

const formButtonClicked = ref(false);

const userInfo = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
});
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
      await authService.register(userInfo.value);
    } catch (error) {
      console.log(error);
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
