<script>
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";
  import CloudUploadIcon from "$lib/icons/CloudUploadIcon.svelte";
  import TrashIcon from "$lib/icons/TrashIcon.svelte";
  import FileIcon from "$lib/icons/FileIcon.svelte";
</script>

<div class={"container mx-auto px-4 py-8 md:py-12 "}>
  <div class="grid gap-8">
    <div class="bg-white dark:bg-gray-950 rounded-lg shadow-sm p-6">
      <h2 class="text-2xl font-bold mb-4">Upload Files</h2>
      <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 flex flex-col items-center justify-center space-y-4 cursor-pointer transition-colors hover:bg-gray-200 dark:hover:bg-gray-750">
        <CloudUploadIcon className="h-12 w-12 text-gray-500 dark:text-gray-400" />
        <p class="text-gray-500 dark:text-gray-400">
          Drag and drop files here or <span class="text-primary font-medium">browse</span>
        </p>
        <Input class="hidden" multiple type="file" />
      </div>
    </div>
    <div class="bg-white dark:bg-gray-950 rounded-lg shadow-sm p-6">
      <h2 class="text-2xl font-bold mb-4">Uploaded Files</h2>
      <div class="space-y-4">
        <div class="flex items-center justify-between bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
          <div class="flex items-center space-x-4">
            <FileIcon className="h-6 w-6 text-gray-500 dark:text-gray-400" />
            <p class="text-gray-700 dark:text-gray-300">example.pdf</p>
          </div>
          <Button class="text-red-500 hover:bg-red-100 dark:hover:bg-red-900" size="icon" variant="ghost">
            <TrashIcon className="h-5 w-5" />
          </Button>
        </div>

        <!-- Similar blocks for other files -->
      </div>
    </div>
  </div>
</div>
