<template>
  <header>
    <div class="logo">
      <img @click="redirectTOMainPage" src="../assets/images/logo.svg" alt="logo" />
    </div>
    <nav class="header-menu">
      <ul>
        <li>Mission</li>
        <li>Services</li>
        <li>FAQ</li>
        <li>Contact</li>
      </ul>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function redirectTOMainPage() {
  router.push({ name: "home-page" });
}
</script>

<style lang="sass" scoped>
@import "@/styles/components/_prior-header"
</style>
