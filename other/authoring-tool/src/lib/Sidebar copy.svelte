<script context="module">
  // retain module scoped expansion state for each tree node
  const _expansionState = {
    /* treeNodeId: expanded <boolean> */
  };
</script>

<script>
  //	import { slide } from 'svelte/transition'
  export let tree = {
    label: "USA",
    children: [
      { label: "Florida", children: [{ label: "Jacksonville" }, { label: "Orlando", children: [{ label: "Disney World" }, { label: "Universal Studio" }, { label: "Sea World" }] }, { label: "Miami" }] },
      { label: "California", children: [{ label: "San Francisco" }, { label: "Los Angeles" }, { label: "Sacramento" }] },
    ],
  };
  const { label, children } = tree;

  let expanded = _expansionState[label] || false;
  const toggleExpansion = () => {
    expanded = _expansionState[label] = !expanded;
  };
  $: arrowDown = expanded;
</script>

<ul>
  <!-- transition:slide -->
  <li>
    {#if children}
      <span on:click={toggleExpansion}>
        <span class="arrow" class:arrowDown>&#x25b6</span>
        {label}
      </span>
      {#if expanded}
        {#each children as child}
          <svelte:self tree={child} />
        {/each}
      {/if}
    {:else}
      <span>
        <span class="no-arrow" />
        {label}
      </span>
    {/if}
  </li>
</ul>
