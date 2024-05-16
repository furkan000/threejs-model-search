<script>
  import { onMount } from "svelte";
  import { run, helloWorld, renameObjectById, findObjectById, model, updateTreeObject } from "./scene";
  import Sidebar from "./Sidebar.svelte";
  import { tree } from "./store";

  let editNodeLabel;
  let editNodeDescription;
  let tree_value;
  let node = {};

  $: node && Object.keys(node).length && updateTreeObject();

  onMount(() => {
    run();
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

<!-- button that triggers functino -->
<!-- <button on:click={test}>Run</button> -->

<body>
  <dialog id="modal" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <h3 class="font-bold text-lg">Edit Node</h3>
      <!-- <p class="py-4">Press ESC key or click the button below to close</p> -->
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
          <!-- if there is a button in form, it will close the modal -->
          <button class="btn">Close</button>
        </form>
      </div>
    </div>
  </dialog>

  <div class="frame">
    <div id="editor">
      <ul class="menu menu-xs rounded-lg w-full">
        <!-- <button on:click={test}>Run</button> -->
        <Sidebar bind:tree={tree_value} {renameObjectById} {openModal} />
      </ul>
    </div>
    <div id="result">
      <canvas style="display: block"></canvas>
    </div>
  </div>
</body>

<style>
  #editor {
    overflow-y: auto;
    /* max-width: 400px;     */
    max-width: fit-content;
    min-width: fit-content;
    padding-right: 2em;
    /* padding-left: 1em; */
    font-family: monospace;
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

  #editor {
    /* --sb-track-color: #d2d2d2; */
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
