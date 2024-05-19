<script>
  import MainView from "$lib/MainView.svelte";
  import { invoke } from "@tauri-apps/api/tauri";

  async function saveFile() {
    const path = `C:\\Users\\Furkan\\Desktop\\file.txt`; // specify your file path
    const contents = "Hello, world!";

    try {
      await invoke("write_to_file", { path, contents });
      console.log("File written successfully");
    } catch (error) {
      console.error("Failed to write file", error);
    }
  }

  saveFile();
</script>

<MainView></MainView>
