<script context="module">
  // retain module scoped expansion state for each tree node
  const _expansionState = {
    /* treeNodeId: expanded <boolean> */
  };
</script>

<script>
  import FileIcon from "./Icons/FileIcon.svelte";
  import FolderIcon from "./Icons/FolderIcon.svelte";
  import PencilSquareIcon from "./Icons/PencilSquareIcon.svelte";

  //	import { slide } from 'svelte/transition'
  export let tree;
  const { label, children } = tree;

  let expanded = _expansionState[label] || false;
  const toggleExpansion = () => {
    expanded = _expansionState[label] = !expanded;
  };
  $: arrowDown = expanded;
</script>

<!-- transition:slide -->
<li>
  {#if children}
    <details open>
      <summary>
        <FolderIcon />
        {label}
        <span class="">
          <PencilSquareIcon />
        </span>
      </summary>
      <ul>
        <!-- {#if expanded} -->
        {#each children as child}
          <svelte:self tree={child} />
        {/each}
        <!-- {/if} -->
      </ul>
    </details>
  {:else}
    <a>
      <FileIcon />
      {label}
      <span class="pr-4">
        <PencilSquareIcon />
      </span>
    </a>
  {/if}
</li>
