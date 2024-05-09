import "./assets/main.css";

import { createApp } from "vue";
import PrimeVue from "primevue/config";
import App from "./App.vue";
import router from "./router";
import "primevue/resources/themes/aura-light-green/theme.css";

const app = createApp(App);

app.use(router);

app.mount("#app");
app.use(PrimeVue);
