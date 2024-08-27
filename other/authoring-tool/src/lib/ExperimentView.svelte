<script>
  import PencilSquareIcon from "./Icons/PencilSquareIcon.svelte";
  import FileIcon from "./Icons/FileIcon.svelte";
  import FolderIcon from "./Icons/FolderIcon.svelte";
</script>

<ul class="menu menu-xs bg-base-200 rounded-lg max-w-xs w-full">
  <li>
    <a class="">
      <FileIcon />
      <span>resume.pdf</span>
      <PencilSquareIcon />
      <span class="pr-4"><PencilSquareIcon /></span>
    </a>
  </li>
  <li>
    <details open>
      <summary class="flex">
        <FolderIcon />
        <span class="flex-1"> My Files </span>

        <PencilSquareIcon />
        <PencilSquareIcon />
      </summary>
      <ul>
        <li>
          <a>
            <FileIcon />
            Project-final.psd
          </a>
        </li>
        <li>
          <a>
            <FileIcon />
            Project-final-2.psd
          </a>
        </li>
        <li>
          <details open>
            <summary>
              <FolderIcon />
              Images
            </summary>
            <ul>
              <li>
                <a>
                  <FileIcon />
                  Screenshot1.png
                </a>
              </li>
              <li>
                <a>
                  <FileIcon />
                  Screenshot2.png
                </a>
              </li>
              <li>
                <details open>
                  <summary>
                    <FolderIcon />
                    Others
                  </summary>
                  <ul>
                    <li>
                      <a>
                        <FileIcon />
                        Screenshot3.png
                      </a>
                    </li>
                  </ul>
                </details>
              </li>
            </ul>
          </details>
        </li>
      </ul>
    </details>
  </li>
  <li>
    <a>
      <FileIcon />
      reports-final-2.pdf
    </a>
  </li>
</ul>
