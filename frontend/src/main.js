import { createApp } from "vue";
import App from "./App.vue";
import router from "@/router";
import { createHead } from "@vueuse/head";
import { createPinia } from "pinia";
import "./styles/main.scss";

createApp(App).use(router).use(createHead()).use(createPinia()).mount("#app");
