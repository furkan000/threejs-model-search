<script>
  import { onMount } from "svelte";
  import { run, helloWorld, renameObjectById, findObjectById, model, updateTreeObject, highlightObjectById } from "./scene";
  import Sidebar from "./Sidebar.svelte";
  import { tree } from "./store";

  let editNodeLabel;
  let editNodeDescription;
  let tree_value;
  let node = {};

  $: node && Object.keys(node).length && updateTreeObject();

  onMount(() => {
    // Delay the initialization to ensure the canvas is correctly sized
    requestAnimationFrame(() => {
      run();
      // Trigger a resize event to ensure correct initial sizing
      window.dispatchEvent(new Event("resize"));
    });
  });

  tree.subscribe((value) => {
    tree_value = value;
  });

  function openModal(nodeId) {
    node = findObjectById(model, nodeId);
    if (!node.description) {
      node.description = "";
    }
    // @ts-ignore
    modal.showModal();
  }

  function applyChanges() {}
</script>

<body>
  <div class="frame">
    <div id="editor">
      <ul class="menu menu-xs rounded-lg w-full">
        <Sidebar bind:tree={tree_value} {renameObjectById} {openModal} {highlightObjectById} />
      </ul>
    </div>
    <div id="result">
      <canvas style="display: block"></canvas>
    </div>
  </div>

  <dialog id="modal" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <h3 class="font-bold text-lg">Edit Node</h3>
      <label class="form-control w-full py-4">
        <div class="label">
          <span class="label-text">Node Name</span>
        </div>
        <input bind:value={node.name} type="text" placeholder="Type here" class="input input-bordered w-full" />
      </label>
      <label class="form-control">
        <div class="label">
          <span class="label-text">Discription</span>
        </div>
        <textarea bind:value={node.description} class="textarea textarea-bordered h-24" placeholder="Empty"></textarea>
      </label>
      <div class="modal-action">
        <form method="dialog">
          <button class="btn">Close</button>
        </form>
      </div>
    </div>
  </dialog>
</body>

<style>
  #editor {
    overflow-y: auto;
    max-width: fit-content;
    min-width: fit-content;
    padding-right: 2em;
    font-family: monospace;
  }

  html {
    box-sizing: border-box;
  }
  *,
  *:before,
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

  #editor {
    --sb-thumb-color: #cacaca;
    --sb-size: 8px;
  }

  #editor::-webkit-scrollbar {
    width: var(--sb-size);
  }

  #editor::-webkit-scrollbar-track {
    background: var(--sb-track-color);
    border-radius: 3px;
  }

  #editor::-webkit-scrollbar-thumb {
    background: var(--sb-thumb-color);
    border-radius: 3px;
  }

  @supports not selector(::-webkit-scrollbar) {
    body {
      scrollbar-color: var(--sb-thumb-color) var(--sb-track-color);
    }
  }
</style>
