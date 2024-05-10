<script>
  import MainView from "./lib/MainView.svelte";
  import Sidebar from "./lib/Sidebar.svelte";

  let tree = {
    label: "USA",
    children: [
      { label: "Florida", children: [{ label: "Jacksonville" }, { label: "Orlando", children: [{ label: "Disney World" }, { label: "Universal Studio" }, { label: "Sea World" }] }, { label: "Miami" }] },
      { label: "California", children: [{ label: "San Francisco" }, { label: "Los Angeles" }, { label: "Sacramento" }] },
    ],
  };

  function handleSummaryClick(event) {
    event.preventDefault();
    // You can add more code here for other actions when the summary is clicked
  }
</script>

<MainView />

<!-- <ul class="menu menu-xs bg-base-200 rounded-lg max-w-xs w-full">
  <Sidebar {tree} />
</ul>

<details>
  <summary on:click={handleSummaryClick}>Details</summary>
  Something small enough to escape casual notice.
</details> -->
