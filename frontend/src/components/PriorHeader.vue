<template>
  <header :class="{ 'mobile-header': screenWidth < 835 }">
    <div class="logo">
      <img alt="logo" src="../assets/images/logo.svg" @click="redirectTOMainPage" />
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
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const screenWidth = ref(null);
const mobileMenu = ref(true);

function displayWindowSize() {
  screenWidth.value = document.documentElement.clientWidth;
}

window.addEventListener("resize", displayWindowSize);

displayWindowSize();

function showHideMenu() {
  mobileMenu.value = mobileMenu.value ? false : true;
}

function redirectTOMainPage() {
  router.push({ name: "home-page" });
}
</script>

<style lang="sass" scoped>
@import "@/styles/components/_prior-header"
</style>
