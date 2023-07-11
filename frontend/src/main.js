import { createApp } from "vue";
import App from "./App.vue";
import router from "@/router";
import { createHead } from "@vueuse/head";
import { plugin, defaultConfig } from "@formkit/vue";
import "@formkit/themes/genesis";

createApp(App).use(router).use(createHead()).use(plugin, defaultConfig).mount("#app");
