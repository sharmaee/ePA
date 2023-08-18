<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <h1>Prepare Prior Authorizations For Approval <span class="blue-text">Approval</span></h1>

    <div class="home-page-btn-wrapper">
      <router-link :to="{ name: 'insurance-navigator-page' }" class="btn-blue"> Get Started </router-link>
      <router-link :to="{ name: 'request-denial-report' }" class="btn-blue"> Report Denial </router-link>
    </div>
  </div>
  <PriorFooter />
</template>

<script setup>
import PriorHeader from "@/components/PriorHeader";
import PriorFooter from "@/components/PriorFooter";
</script>

<style lang="sass" scoped>
@import "../styles/pages/_home-page"
</style>
