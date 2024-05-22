<script>
  import MainView from "./lib/MainView.svelte";
  import Sidebar from "./lib/Sidebar.svelte";
  import ExperimentView from "./lib/ExperimentView.svelte";

  function handleSummaryClick(event) {
    event.preventDefault();
    // You can add more code here for other actions when the summary is clicked
  }
</script>

<MainView />
<!-- <ExperimentView /> -->

<!-- <ul class="menu menu-xs bg-base-200 rounded-lg max-w-xs w-full">
  <Sidebar {tree} />
</ul>

<details>
  <summary on:click={handleSummaryClick}>Details</summary>
  Something small enough to escape casual notice.
</details> -->
