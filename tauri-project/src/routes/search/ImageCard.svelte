<script>
  export let id;
  export let imageUrl = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500";
  export let title = "Search Result Title";
  export let description = "This is a brief description of the search result. It should be concise and informative.";
  import { modelUrl } from "../../lib/store.js";

  function importToEditor() {
    modelUrl.set("http://localhost:5001/download/" + id);
    console.log("http://localhost:5001/download/" + id);
    window.location.href = "/editor";
  }
</script>

<div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden group relative h-full">
  <img src={imageUrl} alt="Search Result" width="300" height="300" class="w-full h-64 object-cover" style="aspect-ratio: 300 / 300; object-fit: cover;" />
  <div class="p-4 h-full flex flex-col justify-between">
    <div>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">{title}</h3>
      <p class="text-gray-600 dark:text-gray-400 line-clamp-3">{description}</p>
    </div>
    <div on:click={importToEditor} class="absolute inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
      <span class="text-white font-semibold">Import to editor</span>
    </div>
  </div>
</div>
