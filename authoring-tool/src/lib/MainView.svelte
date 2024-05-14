<script>
  import { onMount } from "svelte";
  import { run } from "./scene";
  import Sidebar from "./Sidebar.svelte";
  import { tree } from "./store";

  onMount(() => {
    run();
  });

  let tree_value;

  tree.subscribe((value) => {
    tree_value = value;
  });

  function test() {
    console.log(tree_value);
  }
</script>

<!-- button that triggers functino -->
<!-- <button on:click={test}>Run</button> -->

<body>
  <div class="frame">
    <div id="editor">
      <ul class="menu menu-xs rounded-lg max-w-xs w-full">
        <Sidebar bind:tree={tree_value} />
      </ul>
    </div>
    <div id="result">
      <canvas style="display: block"></canvas>
    </div>
  </div>
</body>

<style>
  #editor {
    overflow: auto;
    max-width: 400px;
    /* font-family: monospace; */
    /* padding: 0.5em; */
    /* background: #444; */
    /* color: white; */
  }

  html {
    box-sizing: border-box;
  }
  *,
  k *:before,
  *:after {
    box-sizing: inherit;
  }
  body {
    margin: 0;
  }
  .outer {
  }
  .frame {
    display: flex;
    width: 100vw;
    height: 100vh;
  }
  .frame > * {
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: 50%;
  }

  canvas {
    width: 100%;
    height: 100%;
  }
</style>
