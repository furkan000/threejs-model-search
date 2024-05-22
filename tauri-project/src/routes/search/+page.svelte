<script>
  import ImageCard from "$lib/ImageCard.svelte";
</script>

<!--
// v0 by Vercel.
// https://v0.dev/t/uNEcSQwX82p
-->

<div class="w-full bg-gray-100 dark:bg-gray-900 py-8 px-4 md:px-6">
  <div class="max-w-3xl mx-auto">
    <form class="flex items-center bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-4 h-5 w-5 text-gray-400">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.3-4.3"></path>
      </svg>
      <input class="flex h-10 w-full rounded-md border border-input bg-background text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 flex-1 py-3 px-4 text-gray-700 dark:text-gray-300 focus:outline-none" placeholder="Search for anything..." type="search" style="" />
      <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 bg-gray-900 text-white rounded-r-lg px-6 py-3 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-600 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-200 dark:focus:ring-gray-400"> Search </button>
    </form>
  </div>
</div>
<div class="container mx-auto py-12 px-4 md:px-6">
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
    <ImageCard />
    <ImageCard />
    <ImageCard />
  </div>
</div>
