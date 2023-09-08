<template>
  <header :class="{ 'mobile-header': screenWidth < 835 }">
    <div class="logo">
      <img alt="logo" src="../assets/images/logo.png" @click="redirectToHomePage" />
    </div>
    <img
      v-if="screenWidth < 835"
      src="@/assets/images/mobile-menu.svg"
      alt="mobile-menu"
      class="mobile-menu-img"
      @click="showHideMenu" />
    <nav class="nav" :class="{ 'mobile-menu': screenWidth < 835, hide: mobileMenu }">
      <ul>
        <li>
          <router-link :to="{ name: 'register' }">Start New Patient</router-link>
        </li>
        <li>
          <router-link v-if="authManager.loggedIn" :to="{ name: 'login' }" @click="logoutUser">Log Out</router-link>
          <router-link v-else :to="{ name: 'login' }">Login</router-link>
        </li>
        <!-- <li>
          <a href="https://www.dopriorauth.com/">For Providers</a>
        </li>
        <li>
          <a href="https://www.dopriorauth.com/product/for-life-science-companies">For life science companies</a>
        </li>
        <li>
          <a href="https://www.dopriorauth.com/company/about">About</a>
        </li>
        <li>
          <a href="https://www.dopriorauth.com/company/careers">Careers</a>
        </li> -->
      </ul>
    </nav>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
import { useAuthStore } from "@/stores";

const screenWidth = ref(null);
const mobileMenu = ref(true);

const authManager = useAuthStore();

function displayWindowSize() {
  screenWidth.value = document.documentElement.clientWidth;
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();

function showHideMenu() {
  mobileMenu.value = mobileMenu.value ? false : true;
}

function redirectToHomePage() {
  router.push({ name: "home-page" });
}

async function logoutUser() {
  await authManager.logout();
  window.location.reload();
}
</script>

<style lang="sass" scoped>
@import "@/styles/components/_prior-header"
</style>
