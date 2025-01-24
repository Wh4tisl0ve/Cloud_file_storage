document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const fileListing = document.getElementById("file-listing");
  const uploadForm = document.getElementById("upload-form");

  fileInput.addEventListener("change", () => {
    handleFiles(fileInput);
    uploadFiles(fileInput.files);
  });

  dropZone.addEventListener("click", () => fileInput.click());
  
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drop-zone--over");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drop-zone--over");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drop-zone--over");
    handleFiles(e.dataTransfer);
    uploadFiles(e.dataTransfer.files);
  });

  uploadForm.addEventListener("submit", (e) => {
    e.preventDefault();
    uploadFiles(fileInput.files);
  });

  function handleFiles(dataTransferOrInput) {
    const files = dataTransferOrInput.files;
    fileListing.innerHTML = "";

    const maxFilesToShow = 3;

    for (let i = 0; i < Math.min(files.length, maxFilesToShow); i++) {
      const li = document.createElement("li");
      li.textContent = files[i].webkitRelativePath || files[i].name;
      fileListing.appendChild(li);

      updateThumbnail(dropZone, files[i]);
    }

    if (files.length > maxFilesToShow) {
      const li = document.createElement("li");
      li.textContent = `И ещё ${files.length - maxFilesToShow} файлов...`;
      li.style.fontStyle = "italic";
      fileListing.appendChild(li);
    }
  }

  function uploadFiles(files) {
    if (!files.length) {
      alert("Выберите файлы для загрузки.");
      return;
    }

    const formData = new FormData();

    for (const file of files) {
      formData.append("fileList", file);
      formData.append("filePaths", file.webkitRelativePath || file.name);
    }

    fetch(uploadForm.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
      },
    })
      .then((response) => {
        if (response.ok) {
          location.reload();
        } else {
          alert("Ошибка загрузки файлов.");
        }
      })
      .catch((error) => {
        console.error("Error uploading files:", error);
      });
  }

  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }

    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      const fileTypeIcon = getFileTypeIcon(file.name);
      thumbnailElement.style.backgroundImage = `url('/static/cloud/${fileTypeIcon}')`;
    }
  }

  function getFileTypeIcon(fileName) {
    const fileExtension = fileName.split(".").pop().toLowerCase();

    const fileIcons = {
      pdf: "icons/format/pdf-icon.png",
      doc: "icons/format/docx-icon.png",
      docx: "icons/format/docx-icon.png",
      xls: "icons/format/xls-icon.png",
      xlsx: "icons/format/xlsx-icon.png",
      txt: "icons/format/txt-icon.png",
      zip: "icons/format/zip-icon.png",
      default: "icons/format/default-icon.png",
    };

    return fileIcons[fileExtension] || fileIcons["default"];
  }
});
