<script>
  import { onMount } from "svelte";
  import SmallSearchIcon from "./SmallSearchIcon.svelte";
  import ImageCard from "./ImageCard.svelte";

  onMount(() => {
    document.head.insertAdjacentHTML("beforeend", "<style>html,body{height:100%;background:rgb(243,244,246);}</style>");
  });

  let results = [];
  let inputText = "";
  let numResults = 3;

  function handleKeyPress(event) {
    if (event.key === "Enter") {
       event.preventDefault();
      search();
      inputText = ""; // Optional: to clear the input after pressing enter
    }
  }

  async function search() {
    // console.log(inputText);
    // inputText = "";

    const response = await fetch("http://localhost:5001/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: inputText,
    });
    results = await response.json();
    console.log(results);
  }
</script>

<!-- svelte-ignore a11y-missing-attribute -->
<html>
  <body>
    <header class="relative flex items-center justify-center bg-gray-900 px-6 py-4 dark:bg-gray-950">
      <a class="absolute left-6 flex items-center gap-3" href="http://localhost:5173/">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6 text-gray-400 transition-colors group-hover:text-gray-50">
          <path d="m12 19-7-7 7-7"></path>
          <path d="M19 12H5"></path>
        </svg>
        <span class="text-xl font-semibold text-gray-50">Back</span>
      </a>
      <h1 class="text-xl font-semibold text-gray-50">Search</h1>
      <div class="w-6 h-6"></div>
    </header>

    <!--
// v0 by Vercel.
// https://v0.dev/t/uNEcSQwX82p
-->

    <div class="w-full bg-gray-100 dark:bg-gray-900 py-8 px-4 md:px-6">
      <div class="max-w-3xl mx-auto">
        <form class="flex items-center bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
          <div class="relative w-full">
            <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
              <SmallSearchIcon />
            </div>
            <input bind:value={inputText} on:keypress={handleKeyPress} type="search" id="default-search" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search models based on AI generated descriptions" />
            <button on:click={search} type="submit" class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
          </div>
        </form>
      </div>
    </div>
    <div class="container mx-auto py-12 px-4 md:px-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        <!--             "id": id,
            "generated_description": gen_desc,
            "title": title,
            "description": desc,
            "thumbnail": thumb_url -->

        {#each results as result}
          <ImageCard id={result.id} imageUrl={result.thumbnail} title={result.title} description={result.generatedDescription} />
        {/each}

        <!-- <ImageCard /> -->
        <!-- <ImageCard /> -->
        <!-- <ImageCard /> -->
      </div>
    </div>
  </body>
</html>

<style>
  html,
  body {
    height: 100%;
    background: rgb(243 244 246);
  }
</style>
