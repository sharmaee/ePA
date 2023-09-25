!
<template>
  <div class="smart-engine-success-wrapper">
    <div class="smart-engine-success-img">
      <img src="@/assets/images/modal-green-checkmark.svg" alt="success" />
    </div>
    <h2>Complete!</h2>
    <p>Thanks to your efforts, our patients are one step closer to achieving their health goals.</p>
    <div class="smart-engine-start-new-patient">
      <button @click="redirectToHomePage">Start New Patient</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function redirectToHomePage() {
  router.push({ name: "home-page" });
}
</script>

<style lang="scss" scoped>
@import "../styles/pages/_smart-engine-container.scss";
</style>
