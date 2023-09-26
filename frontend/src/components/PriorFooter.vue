<template>
  <footer>
    <div class="left-footer">
      <span>©2023 dopriorauth.com </span>
    </div>
    <div class="center-footer">
      <small>{{ appVersion }}</small>
    </div>
    <div class="right-footer">
      <ul>
        <li>Terms and Conditions</li>
        <li>·</li>
        <li>Privacy Policy</li>
      </ul>
    </div>
  </footer>
</template>

<script setup>
const appVersion = process.env.VUE_APP_VERSION;
</script>

<style lang="sass" scoped>
@import "@/styles/components/_prior-footer"
</style>
