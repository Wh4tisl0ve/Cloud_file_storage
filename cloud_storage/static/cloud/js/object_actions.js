export function create_object(nameObject) {
    const objectInfo = { nameObject: nameObject };
    if (validate_name(nameObject)) {
        alert('Имя объекта не должно содержать /, % или #');
    }
    else {
        send_request('create_object', 'POST', JSON.stringify(objectInfo));
    }
}

export function delete_object(nameObject) {
    const objectInfo = { nameObject: nameObject };
    send_request('delete_object', 'DELETE', JSON.stringify(objectInfo));
}

export function rename_object(oldName, newName) {
    const nameData = { oldName: oldName, newName: newName };

    if (validate_name(newName)) {
        alert('Имя объекта не должно содержать /, % или #');
        return;
    }

    const getExtension = (filename) => {
        return filename.slice((Math.max(0, filename.lastIndexOf(".")) || Infinity) + 1);
    };

    const extOld = getExtension(oldName);
    const extNew = getExtension(newName);

    if (extOld !== extNew && (extOld || extNew)) {
        if (confirm(`Расширение(.${extOld}) файла будет изменено`)) {
            send_request('rename_object', 'PATCH', JSON.stringify(nameData));
        }
    } else {
        send_request('rename_object', 'PATCH', JSON.stringify(nameData));
    }
}

export function download_object(nameObject) {
    const path = new URL(document.location.toString()).searchParams.get("path") || "";

    const params = new URLSearchParams();
    params.append('path', path);
    params.append('nameObject', nameObject);
    window.location.href = `/download_object/?${params.toString()}`
}

export function upload_object(files) {
    const formData = new FormData();

    for (const file of files) {
        formData.append("fileList", file);
        if (file.webkitRelativePath) {
            formData.append("filePaths", file.webkitRelativePath);
        }
    }

    send_request('upload_object', 'POST', formData);
}

function send_request(url, method, data) {
    const params = new URL(document.location.toString()).searchParams;

    fetch(`/${url}/?${params}`, {
        method: method,
        headers: {
            'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: data
    }).then((response) => {
        if (response.ok) {
            location.reload();
        } else if (response.status == 409) {
            alert("Объект с таким именем уже существует");
        }
        else if (response.status == 400) {
            alert("Ошибка в имени файла");
        }
        else {
            alert("Невозможно выполнить действие");
        }
    }).catch((error) => {
        console.error("Ошибка сети:", error);
    });
}

function validate_name(name) {
    const invalidChars = /[/%#]/;

    return invalidChars.test(name);
}