<script>
  import BackIcon from "./BackIcon.svelte";
  import AnnotateIcon from "./AnnotateIcon.svelte";
  import ThreeDimIcon from "./ThreeDimIcon.svelte";
  import UploadIcon from "./Icons/UploadIcon.svelte";
</script>

<!--
// v0 by Vercel.
// https://v0.dev/t/L8nO37MW4qo
-->

<main class="flex flex-col h-screen">
  <header class="flex items-center justify-between bg-gray-900 px-6 py-4 dark:bg-gray-950">
    <a class="flex items-center gap-3" href="#">
      <BackIcon />
      <span class="text-xl font-semibold text-gray-50">Back</span>
    </a>
    <h1 class="text-xl font-semibold text-gray-50">Authoring Tool</h1>
    <div class="w-6 h-6"></div>
  </header>
  <body class="flex h-full w-full flex-col items-center justify-center gap-16 bg-gray-100 px-6 py-16 dark:bg-gray-950">
    <div class="container mx-auto grid max-w-6xl grid-cols-1 gap-16 md:grid-cols-3">
      <a class="group flex flex-col items-center justify-center gap-8 rounded-xl bg-white p-16 text-center shadow-sm transition-colors hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800" href="#">
        <div class="flex h-24 w-24 items-center justify-center rounded-full bg-blue-500 text-white group-hover:bg-blue-600">
          <UploadIcon />
        </div>
        <div>
          <h3 class="text-2xl font-semibold tracking-tight">Upload Document</h3>
          <p class="mt-2 text-gray-500 dark:text-gray-400 text-lg">Upload your documents for processing.</p>
        </div>
      </a>
      <a class="group flex flex-col items-center justify-center gap-8 rounded-xl bg-white p-16 text-center shadow-sm transition-colors hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800" href="#">
        <div class="flex h-24 w-24 items-center justify-center rounded-full bg-green-500 text-white group-hover:bg-green-600">
          <ThreeDimIcon />
        </div>
        <div>
          <h3 class="text-2xl font-semibold tracking-tight">Upload Model</h3>
          <p class="mt-2 text-gray-500 dark:text-gray-400 text-lg">Upload your models for processing.</p>
        </div>
      </a>
      <a class="group flex flex-col items-center justify-center gap-8 rounded-xl bg-white p-16 text-center shadow-sm transition-colors hover:bg-gray-50 dark:bg-gray-900 dark:hover:bg-gray-800" href="/editor">
        <div class="flex h-24 w-24 items-center justify-center rounded-full bg-yellow-500 text-white group-hover:bg-yellow-600">
          <AnnotateIcon />
        </div>
        <div>
          <h3 class="text-2xl font-semibold tracking-tight">Annotate Model</h3>
          <p class="mt-2 text-gray-500 dark:text-gray-400 text-lg">Annotate your models for processing.</p>
        </div>
      </a>
    </div>
  </body>
</main>
