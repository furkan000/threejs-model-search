<script>
  import ChatBubbleOvalLeft from "./Icons/ChatBubbleOvalLeft.svelte";
  import FileIcon from "./Icons/FileIcon.svelte";
  import FolderIcon from "./Icons/FolderIcon.svelte";
  import PencilSquareIcon from "./Icons/PencilSquareIcon.svelte";

  export let tree;
  export let renameObjectById;
  export let openModal;

  let isEditing = false;
  let inputElement;
  let isEditCompleteHandled = false;

  function startEditing() {
    isEditing = true;
    isEditCompleteHandled = false;
    // $: if (isEditing) {
    //   setTimeout(() => {
    //     inputElement.focus();
    //     inputElement.select();
    //   }, 0);
    // }
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
    renameObjectById(tree.id, tree.label);
  }
</script>

<li>
  {#if tree.children}
    <details open>
      <summary class="flex">
        <FolderIcon />
        {#if isEditing}
          <input bind:this={inputElement} bind:value={tree.label} on:blur={handleBlur} on:keydown={onEditComplete} />
        {:else}
          <span on:dblclick={startEditing} class="flex-1">{tree.label}</span>
        {/if}
        <span class="clickable" on:click={startEditing}>
          <PencilSquareIcon />
        </span>
        <span class="clickable" on:click={openModal(tree.id)}>
          <ChatBubbleOvalLeft />
        </span>
      </summary>
      <ul>
        {#each tree.children as child}
          <svelte:self {...$$props} tree={child} />
        {/each}
      </ul>
    </details>
  {:else}
    <a>
      <FileIcon />
      {#if isEditing}
        <input bind:this={inputElement} bind:value={tree.label} on:blur={handleBlur} on:keydown={handleKeyDown} />
      {:else}
        <span on:dblclick={startEditing}>{tree.label}</span>
      {/if}
      <span class="clickable" on:click={startEditing}>
        <PencilSquareIcon />
      </span>
      <span class="clickable pr-4 {tree.description ? 'text-yellow-600' : ''}" on:click={openModal(tree.id)}> <ChatBubbleOvalLeft /> </span>
    </a>
  {/if}
</li>

<style>
  .clickable {
    cursor: pointer;
  }
</style>
