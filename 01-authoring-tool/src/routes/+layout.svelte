<script>
  import "../app.css";

  import { onMount } from "svelte";
  import { modelUrl } from "$lib/store.js";
  let savestore = false;
  $: if (savestore && $modelUrl) {
    window.sessionStorage.setItem("store", JSON.stringify($modelUrl));
  }
  onMount(async () => {
    let ses = window.sessionStorage.getItem("store");
    if (ses) {
      console.log("sob-- ~ loading ses", ses);
      $modelUrl = JSON.parse(ses);
    }
    savestore = true;
  });
</script>

<slot />
