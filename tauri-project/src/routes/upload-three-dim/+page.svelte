<script>
  import Upload from "$lib/Upload.svelte";
  import UploadFileIcon from "$lib/Icons/UploadFileIcon.svelte";
  import UploadThreeDim from "$lib/Icons/UploadThreeDim.svelte";

  let file;
</script>

<Upload folder="threedim" icon={UploadThreeDim} title="Upload Model" uploadTitle="Model Upload" fileTitle="Uploaded Models" showExportToThree></Upload>
