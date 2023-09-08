<template>
  <PriorHeader />
  <div class="confirm-email-wrapper">
    <h1 class="registration-page-title">Account Registered!</h1>
    <div class="form">
      <p>Your account has successfully been created. Click below to Login to your account.</p>
      <button @click="redirectionToLoginPage">Continue To Login</button>
    </div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import authService from "@/services/authService";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
import { tryParseApiErrors } from "@/utils";

const loading = ref(false);
const success = ref(true);
const failure = ref(false);
const route = useRoute();
const router = useRouter();
const errors = ref([]);

onMounted(async () => {
  try {
    await authService.confirmEmail(route.params.user_id, route.params.token);
    success.value = true;
  } catch (error) {
    errors.value = tryParseApiErrors(error);
    failure.value = true;
  }
  loading.value = false;
});

function redirectionToLoginPage() {
  router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_authorisation-forms.scss";
</style>
