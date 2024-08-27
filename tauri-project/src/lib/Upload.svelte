<!--
// v0 by Vercel.
// https://v0.dev/t/7Wo74qHXHti
-->

<script>
  import { modelUrl } from "./store.js";
  import UploadFileIcon from "$lib/Icons/UploadFileIcon.svelte";
  import { onMount } from "svelte";
  import { calcKoverI } from "three/examples/jsm/curves/NURBSUtils.js";

  export let folder;
  export let showExportToThree = false;
  export let title;
  export let uploadTitle;
  export let fileTitle;
  export let icon;

  let files = [];
  let fileInput;

  function triggerFileInput() {
    fileInput.click();
  }

  onMount(async function () {
    await getFiles();

    let dropArea = document.getElementById("drop-area");

    ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ["dragenter", "dragover"].forEach((eventName) => {
      dropArea.addEventListener(eventName, () => dropArea.classList.add("highlight"), false);
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, () => dropArea.classList.remove("highlight"), false);
    });

    dropArea.addEventListener("drop", handleDrop, false);

    function handleDrop(e) {
      let dt = e.dataTransfer;
      let files = dt.files;
      handleFiles(files);
    }

    function handleFiles(files) {
      [...files].forEach(uploadFile);
    }
  });

  async function getFiles() {
    const response = await fetch("http://localhost:5000/" + folder);
    if (response.ok) files = (await response.json()).files;
  }

  async function deleteFile(fileName) {
    const response = await fetch(`http://localhost:5000/${folder}/delete/${fileName}`, {
      method: "POST",
    });
    await getFiles();
  }

  function uploadFile(file) {
    let url = "http://localhost:5000/" + folder + "/upload";
    let formData = new FormData();
    formData.append("file", file);

    fetch(url, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        // if (data.filename) {
        getFiles();
        // }
      })
      .catch(console.error);
  }

  function handleFileChange(event) {
    // const file = event.target.files[0];
    if (file) {
      uploadFile(file);
    }
  }

  function gotoEditor(file) {
    modelUrl.set("http://localhost:5000/" + folder + "/download/" + file);
    window.location.href = "http://localhost:5173/editor";
  }
</script>

<header class="relative flex items-center justify-center bg-gray-900 px-6 py-4 dark:bg-gray-950">
  <a class="absolute left-6 flex items-center gap-3" href="http://localhost:5173/">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6 text-gray-400 transition-colors group-hover:text-gray-50">
      <path d="m12 19-7-7 7-7"></path>
      <path d="M19 12H5"></path>
    </svg>
    <span class="text-xl font-semibold text-gray-50">Back</span>
  </a>
  <h1 class="text-xl font-semibold text-gray-50">{title}</h1>
  <div class="w-6 h-6"></div>
</header>

<body>
  <div class="container mx-auto px-4 py-8 md:py-12">
    <div class="grid gap-8">
      <div class="bg-white dark:bg-gray-950 rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold">{uploadTitle}</h2>
          <div class="flex items-center space-x-2">
            <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-gray-500 dark:text-gray-400">
                <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>
            <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-gray-500 dark:text-gray-400">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 16v-4"></path>
                <path d="M12 8h.01"></path>
              </svg>
            </button>
          </div>
        </div>
        <div id="drop-area" class="bg-gray-100 dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 flex flex-col items-center justify-center space-y-4 cursor-pointer transition-colors hover:bg-gray-200 dark:hover:bg-gray-750">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-12 w-12 text-gray-500 dark:text-gray-400">
            <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path>
            <path d="M12 12v9"></path>
            <path d="m16 16-4-4-4 4"></path>
          </svg>
          <p class="text-gray-500 dark:text-gray-400">Drag and drop files here or <span class="text-primary font-medium">browse</span></p>
          <input on:change={handleFileChange} class="h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 hidden" type="file" />
        </div>
      </div>
      <div class="bg-white dark:bg-gray-950 rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold">{fileTitle}</h2>
          <div class="flex items-center space-x-2">
            <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-gray-500 dark:text-gray-400">
                <line x1="10" x2="21" y1="6" y2="6"></line>
                <line x1="10" x2="21" y1="12" y2="12"></line>
                <line x1="10" x2="21" y1="18" y2="18"></line>
                <path d="M4 6h1v4"></path>
                <path d="M4 10h2"></path>
                <path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"></path>
              </svg>
            </button>
            <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 w-10">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-gray-500 dark:text-gray-400">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
              </svg>
            </button>
          </div>
        </div>
        <div id="file-list" class="space-y-4">
          {#each files as file}
            <div id={file} class="flex items-center justify-between bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
              <div class="flex items-center space-x-4">
                <!-- <UploadFileIcon></UploadFileIcon> -->
                <svelte:component this={icon} />
                <p class="text-gray-700 dark:text-gray-300">{file}</p>
              </div>
              <div>
                {#if showExportToThree}
                  <button on:click={() => gotoEditor(file)} class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:text-accent-foreground h-10 w-10 text-green-500 hover:bg-red-100 dark:hover:bg-green-900">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
                      <path d="M5 3v16h16" />
                      <path d="m5 19 6-6" /><path d="m2 6 3-3 3 3" />
                      <path d="m18 16 3 3-3 3" />
                    </svg>
                  </button>
                {/if}
                <button on:click={() => deleteFile(file)} class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:text-accent-foreground h-10 w-10 text-red-500 hover:bg-red-100 dark:hover:bg-red-900">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</body>
