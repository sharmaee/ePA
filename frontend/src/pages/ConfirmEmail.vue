<template>
  <PriorHeader />
  <div class="confirm-email-wrapper">Confirm email</div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import authService from "@/services/authService";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

const loading = ref(false);
const success = ref(true);
const failure = ref(false);
const route = useRoute();
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
</script>

<style lang="scss" scoped>
// @import "../styles/pages/_confirm-email.scss";
</style>
