<template>
  <PriorHeader />
  <div class="home-page-wrapper">
    <div class="shadow-ellipse shadow-ellipse-right"></div>
    <h1>Prepare Prior Authorizations For <span class="blue-text">Approval</span></h1>
    <div class="home-page-btn-wrapper">
      <router-link :to="{ name: 'insurance-navigator-page' }" class="btn-blue">Get Started</router-link>
      <router-link :to="{ name: 'report-denial' }" class="btn-blue">Denial Next Steps</router-link>
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
