<script>
  import { onMount } from "svelte";

  let files = [];

  onMount(async function () {
    await getFiles();
  });

  async function getFiles() {
    const response = await fetch("http://localhost:5000");
    if (response.ok) files = (await response.json()).files;
  }

  async function deleteFile(fileName) {
    const response = await fetch(`http://localhost:5000/delete/${fileName}`, {
      method: "POST",
    });
    await getFiles();
  }

  function uploadFile(file) {
    let url = "http://localhost:5000/upload";
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

  function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      uploadFile(file);
    }
  }
</script>

<!-- <MainView /> -->
<!-- <Overview /> -->
<!-- <UploadThreeDim /> -->

<input type="file" on:change={handleFileChange} />
<br />
<br />

{#each files as file}
  <p>
    {file}
    <button on:click={() => deleteFile(file)}>Delete</button>
  </p>
{/each}
