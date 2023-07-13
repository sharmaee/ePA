<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <h1>The <span class="lilac-text">Wegovy</span> Insurance Navigator.</h1>
    <div class="home-page-main-block">
      <div class="home-page-img">
        <img src="../assets/images/man.png" alt="man" />
      </div>
      <div class="home-page-form">
        <h2>Start a New Request</h2>
      </div>
    </div>
  </div>
  <PriorFooter />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { mainServices } from "@/services/mainServices";
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";

const availableSearchOptions = ref(null);

onMounted(() => {
  getAvailableSearchOptions();
});
async function getAvailableSearchOptions() {
  availableSearchOptions.value = await mainServices.availableSearchOptions();
}
</script>

<style lang="sass" scoped>
@import "../styles/pages/_home-page"
</style>
