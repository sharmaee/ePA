<template>
  <PriorHeader />
  <div class="registered-form-wrapper">
    <h1 class="registration-page-title">Login</h1>
    <div class="form">
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
      <button @click="loginUser">Login</button>

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
  email: "",
  password: "",
});

// Validators
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

async function loginUser() {
  formButtonClicked.value = true;

  if (isEmailValid.value && isPasswordValid.value) {
    try {
      await authService.login(userInfo.value);
    } catch (error) {
      console.log(error);
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
