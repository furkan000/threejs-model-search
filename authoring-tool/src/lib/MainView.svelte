<script>
  import { onMount } from "svelte";
  import { run } from "../scene";
  let el;
  onMount(() => {
    run(el);
  });
</script>

<body>
  <div class="frame">
    <div id="editor">explaintion of example on left or the code for it would go here</div>
    <div id="result">
      <canvas style="display: block"></canvas>
    </div>
  </div>
</body>

<style>
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
  #editor {
    max-width: 300px;
    /* font-family: monospace; */
    padding: 0.5em;
    background: #444;
    /* color: white; */
  }
  canvas {
    width: 100%;
    height: 100%;
  }
</style>
