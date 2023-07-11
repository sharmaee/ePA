<template>
  <router-view />
</template>

<script setup>
import { useHead } from "@vueuse/head";

useHead({
  link: [
    {
      rel: "icon",
      type: "image/png",
      href: require("@/assets/images/favicon-16x16.png"),
    },
  ],
});
</script>
