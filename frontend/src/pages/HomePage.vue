<template>
  <PriorHeader />
  <div class="home-page-content">
    <div class="left-content">
      <h2>Neque porro <span>Auisquam</span> est hui dolorem ipsum.</h2>
    </div>
    <div class="right-content">
      <h2>Start a New Request</h2>
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

.home-page-content
  display: flex

  .left-content
    width: 50%
    display: flex
    align-items: center
    justify-content: center

    h2
      font-size: 64px
      font-weight: 700
      width: 90%

      span
        color: #556FF3
  .right-content
    width: 50%
</style>
