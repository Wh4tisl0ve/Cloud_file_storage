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

        const validation = newName.includes('/') ? isValidObjectName(newName.slice(0, -1)) : isValidObjectName(newName);

        if (!validation.valid) {
            alert(validation.message);
        } else {
            rename_object(oldName, newName);
        }
    }
});


function handleCreateObject(type_object) {
    const name_file = prompt("Введите название объекта:", '');
    const validation = isValidObjectName(name_file);
    if (name_file) {
        if (!validation.valid) {
            alert(validation.message);
        } else {
            const objectName = type_object === "folder" ? `${name_file.replace(/^\/+|\/+$/g, '')}/` : name_file;
            create_object(objectName);
        }
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
        oneFileInput.value = "";
    });

    manyFileInput.addEventListener("change", () => {
        upload_object(manyFileInput.files);
        manyFileInput.value = "";
    });

    uploadFileButton.addEventListener("click", function () {
        document.getElementById("one-file-picker").click();
    });

    uploadFolderButton.addEventListener("click", function () {
        document.getElementById("many-file-picker").click();
    });
});

function isValidObjectName(name) {
    const forbiddenChars = /[\\/:*?"<>|%#]/;

    if (!name || name.trim().length === 0) {
        return { valid: false, message: "Имя объекта не может быть пустым" };
    }

    if (name.length > 40) {
        return { valid: false, message: "Имя объекта слишком длинное (макс. 40 символов)" };
    }

    if (forbiddenChars.test(name)) {
        return { valid: false, message: "Имя содержит запрещенные символы: \\ / : * ? \" < > | %" };
    }

    if (/^\/+$/.test(name)) {
        return { valid: false, message: "Недопустимое имя объекта" };
    }

    return { valid: true, message: "OK" };
}