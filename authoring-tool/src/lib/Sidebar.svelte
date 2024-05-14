<script>
  import FileIcon from "./Icons/FileIcon.svelte";
  import FolderIcon from "./Icons/FolderIcon.svelte";
  import PencilSquareIcon from "./Icons/PencilSquareIcon.svelte";

  export let tree;

  let isEditing = false;
  let label = tree.label;
  let inputElement;
  let isEditCompleteHandled = false;

  function startEditing() {
    isEditing = true;
    isEditCompleteHandled = false;
    $: if (isEditing) {
      setTimeout(() => {
        inputElement.focus();
        inputElement.select();
      }, 0);
    }
  }

  function stopEditing() {
    if (isEditCompleteHandled) return;
    isEditCompleteHandled = true;
    isEditing = false;
    onEditComplete();
  }

  function handleBlur() {
    stopEditing();
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      stopEditing();
    }
  }

  function onEditComplete() {
    console.log("Editing completed:", label);
    // Add any additional logic you want to handle when editing is done
  }
</script>

<li>
  {#if tree.children}
    <details open>
      <summary>
        <FolderIcon />
        {#if isEditing}
          <input bind:this={inputElement} bind:value={label} on:blur={handleBlur} on:keydown={handleKeyDown} />
        {:else}
          <span on:dblclick={startEditing}>{label}</span>
        {/if}
        <span class="clickable" on:click={startEditing}>
          <PencilSquareIcon />
        </span>
      </summary>
      <ul>
        {#each tree.children as child}
          <svelte:self tree={child} />
        {/each}
      </ul>
    </details>
  {:else}
    <a>
      <FileIcon />
      {#if isEditing}
        <input bind:this={inputElement} bind:value={label} on:blur={handleBlur} on:keydown={handleKeyDown} />
      {:else}
        <span on:dblclick={startEditing}>{label}</span>
      {/if}
      <span class="clickable pr-4" on:click={startEditing}>
        <PencilSquareIcon />
      </span>
    </a>
  {/if}
</li>

<style>
  .clickable {
    cursor: pointer;
  }
</style>
