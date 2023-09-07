<template>
  <PriorHeader />
  <div class="registered-form-wrapper">
    <h1 class="registration-page-title">Login</h1>
    <div class="form">
      <div class="your-email">
        <label for="your-email">Email Address</label>
        <input id="your-email" v-model="credentials.email" type="text" placeholder="example@findsunrise.com" />
        <span v-if="!isEmailValid && formButtonClicked" class="input-error-notification">
          Please enter a valid email address.
        </span>
      </div>
      <div class="password">
        <label for="password">Password</label>
        <input id="password" v-model="credentials.password" type="password" />
        <span v-if="!isPasswordValid && formButtonClicked" class="input-error-notification">
          Please create a password with more than 10 characters, at least 1 uppercase and 1 lowercase letter, 1 number,
          and 1 symbol.
        </span>
      </div>
      <button @click="loginUser">Login</button>

      <div class="auxiliary-account-links">
        <router-link :to="{ name: 'password-reset-request' }" class="forgot-pass-link">Forgot Password ?</router-link>
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
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores";

const formButtonClicked = ref(false);
const router = useRouter();
const authStore = useAuthStore();

const credentials = ref({
  email: "",
  password: "",
});

// Validators
const isEmailValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const email = credentials.value.email;
  return email !== "" && emailPattern.test(email);
});

const isPasswordValid = computed(() => {
  const password = credentials.value.password;
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{11,}$/;

  return passwordPattern.test(password);
});

async function loginUser() {
  formButtonClicked.value = true;

  if (isEmailValid.value && isPasswordValid.value) {
    try {
      let otpConfig = await authStore.login(credentials.value);

      console.log("Login successful!", otpConfig);
      await authStore.loginStep2NotRequired();

      router.push({ name: "home-page" });
    } catch (error) {
      console.error("Login error:", error);
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
<!-- "email": "liudmyla@lamarhealth.com",
"password": "Y$nzoH4Tng4f" -->
