import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: vitePreprocess(),

  plugins: [
    svelte({
      onwarn(warning, defaultHandler) {
        // don't warn on <marquee> elements, cos they're cool
        if (warning.code.includes("A11y")) return;

        // handle all other warnings normally
        defaultHandler(warning);
      },
    }),
  ],
};
