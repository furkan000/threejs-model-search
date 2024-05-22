<script>
  import Upload from "$lib/Upload.svelte";
  import UploadFileIcon from "$lib/Icons/UploadFileIcon.svelte";
</script>

<Upload folder="files" icon={UploadFileIcon} title="Upload Documents" uploadTitle="Document Upload" fileTitle="Uploaded Documents" />
