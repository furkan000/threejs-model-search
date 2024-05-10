<script>
  import FileIcon from "./Icons/FileIcon.svelte";
  import FolderIcon from "./Icons/FolderIcon.svelte";
  import PencilSquareIcon from "./Icons/PencilSquareIcon.svelte";

  export let tree;
  const { label, children } = tree;

  let editable = false;
  let editedLabel = label;
  let expanded = false; // Simplified expanded logic for the example
  let inputElement;

  const toggleEdit = (event) => {
    event.preventDefault();
    editable = !editable;
    if (editable) {
      setTimeout(() => {
        inputElement.focus();
      }, 0); // Focus after the DOM updates
    } else {
      // Optionally update the tree label here if needed
    }
  };

  const handleInput = (event) => {
    editedLabel = event.target.value;
  };

  const handleKeyDown = (event) => {
    // Pressing Enter saves the edit
    if (event.key === "Enter") {
      toggleEdit();
    }
  };

  const handleDoubleClick = () => {
    if (!editable) {
      toggleEdit();
    }
  };
</script>

<li>
  {#if children}
    <details open>
      <summary on:dblclick={handleDoubleClick}>
        <FolderIcon />
        {#if editable}
          <input type="text" bind:this={inputElement} bind:value={editedLabel} on:keydown={handleKeyDown} on:blur={toggleEdit} />
        {:else}
          {label}
        {/if}
        <span class="clickable" on:click={toggleEdit}>
          <PencilSquareIcon />
        </span>
      </summary>
      <ul>
        {#each children as child}
          <svelte:self tree={child} />
        {/each}
      </ul>
    </details>
  {:else}
    <a on:dblclick={handleDoubleClick}>
      <FileIcon />
      {#if editable}
        <input type="text" bind:this={inputElement} bind:value={editedLabel} on:keydown={handleKeyDown} on:blur={toggleEdit} />
      {:else}
        {label}
      {/if}
      <span class="clickable pr-4" on:click={toggleEdit}>
        <PencilSquareIcon />
      </span>
    </a>
  {/if}
</li>
