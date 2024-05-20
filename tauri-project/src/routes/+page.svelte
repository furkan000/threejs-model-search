<script>
  import MainView from "$lib/MainView.svelte";
  import Overview from "$lib/Overview.svelte";
  import UploadThreeDim from "$lib/UploadThreeDim.svelte";
  import { onMount } from "svelte";

  let files = "[]";

  onMount(async function () {
    await getFiles();
  });

  async function getFiles() {
    const response = await fetch("http://localhost:5000");
    files = (await response.json()).files;
  }

  async function deleteFile(fileName) {
    const response = await fetch(`http://localhost:5000/delete/${fileName}`, {
      method: "POST",
    });
    await getFiles();
  }

  function uploadFile(file) {
      let url = "/upload";
      let formData = new FormData();
      formData.append("file", file);

      fetch(url, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.message);
          if (data.filename) {
            getFiles();
          }
        })
        .catch(console.error);
    }

    // dropArea.addEventListener("drop", handleDrop, false);

    function handleFiles(files) {
      console.log(files);
      [...files].forEach(uploadFile);
    }


</script>

<!-- <MainView /> -->
<!-- <Overview /> -->
<!-- <UploadThreeDim /> -->

<input type="file" on:drop={(files) => handleDrop(file)} />
<br/>
<br/>

{#each files as file}
  <p>
    {file}
    <button on:click={() => deleteFile(file)}>Delete</button>
  </p>
{/each}