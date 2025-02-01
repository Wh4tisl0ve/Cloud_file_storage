import { delete_object, rename_object, create_object, download_object, upload_object } from './object_actions.js';

document.addEventListener('DOMContentLoaded', function () {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
        new bootstrap.Popover(popoverTriggerEl, {
            html: true,
            sanitize: false
        });
    });
});

/* create */

document.addEventListener("DOMContentLoaded", () => {
    const createFileButton = document.getElementById("create-file-button");
    const createFolderButton = document.getElementById("create-folder-button");

    createFileButton.addEventListener("click", () => handleCreateObject("file"));

    createFolderButton.addEventListener("click", () => handleCreateObject("folder"));
});

/* delete */

document.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('delete-btn')) {
        const objectName = e.target.getAttribute('data-object-name');
        if (confirm(`Вы уверены, что хотите удалить объект "${objectName}"?`)) {
            delete_object(objectName);
        }
    }
});

/* download */

document.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('download-btn')) {
        const objectName = e.target.getAttribute('data-object-name');
        download_object(objectName);
    }
});

/* rename */

document.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('rename-btn')) {
        const oldName = e.target.getAttribute('data-object-name');
        const newName = prompt("Введите новое название объекта:", oldName);
        rename_object(oldName, newName);
    }
});


function handleCreateObject(type_object) {
    const name_file = prompt("Введите название объекта:", '');
    if (name_file && name_file.length < 15) {
        const objectName = type_object === "folder" ? `${name_file.replace(/^\/+|\/+$/g, '')}/` : name_file;
        create_object(objectName);
    } else {
        alert("Имя объекта должно быть не более 15 символов");
    }
}

/* upload */

document.addEventListener("DOMContentLoaded", () => {
    const uploadFileButton = document.getElementById("upload-file-btn");
    const uploadFolderButton = document.getElementById("upload-folder-btn");

    const oneFileInput = document.getElementById("one-file-picker");
    const manyFileInput = document.getElementById("many-file-picker");

    oneFileInput.addEventListener("change", () => {
        upload_object(oneFileInput.files);
    });

    manyFileInput.addEventListener("change", () => {
        upload_object(manyFileInput.files);
    });

    uploadFileButton.addEventListener("click", function () {
        document.getElementById("one-file-picker").click();
    });

    uploadFolderButton.addEventListener("click", function () {
        document.getElementById("many-file-picker").click();
    });
});