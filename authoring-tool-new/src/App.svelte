<script>
  import { onMount } from "svelte";
  import { createScene } from "./lib/scene";
  import Sidebar from "./lib/Sidebar.svelte";

  let el;
  onMount(() => {
    createScene(el);
  });
</script>

<main>
  <div id="viewport">
    <canvas bind:this={el} style="display: block;" />
  </div>
  <div id="sidebar"></div>
</main>

<style>
  #viewport {
    position: absolute;
    left: 0;
    right: 350px;
    bottom: 0;
  }

  #sidebar {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 350px;
    background: #eee;
    overflow: auto;
  }
</style>
