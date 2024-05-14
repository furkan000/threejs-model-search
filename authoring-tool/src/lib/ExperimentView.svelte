<script>
  import { onMount } from "svelte";
  import { count } from "./experiment.js";
  import { writable } from "svelte/store";

  let count_value;

  count.subscribe((value) => {
    count_value = value;
  });
</script>

<main>
  <input bind:value={$count} />
</main>
