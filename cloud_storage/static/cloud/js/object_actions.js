export function create_object(nameObject) {
    const objectInfo = { nameObject: nameObject };
    send_request('create_object', 'POST', JSON.stringify(objectInfo));
}

export function delete_object(nameObject) {
    const objectInfo = { nameObject: nameObject };
    send_request('delete_object', 'DELETE', JSON.stringify(objectInfo));
}

export function rename_object(oldName, newName) {
    const nameData = { oldName: oldName, newName: newName };
    send_request('rename_object', 'PATCH', JSON.stringify(nameData));
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
        formData.append("fileList", file, file.webkitRelativePath || file.name);
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
        } else {
            alert("Невозможно выполнить действие. Проверьте имя объекта, оно не должно содержать более 15 символов");
        }
    }).catch((error) => {
        console.error("Ошибка сети:", error);
    });
}
