export function create_object(nameObject) {
    const objectInfo = { nameObject: nameObject };
    send_request('create_object', 'POST', objectInfo);
}

export function delete_object(nameObject) {
    const objectInfo = { nameObject: nameObject };
    send_request('delete_object', 'DELETE', objectInfo);
}

export function rename_object(oldName, newName) {
    const nameData = { oldName: oldName, newName: newName };
    send_request('rename_object', 'PATCH', nameData);
}

export function download_object(nameObject) {
    const path = new URL(document.location.toString()).searchParams.get("path") || "";

    const params = new URLSearchParams();
    params.append('path', path);
    params.append('nameObject', nameObject);
    window.location.href = `/download_object/?${params.toString()}`
}

function send_request(url, method, data) {
    const params = new URL(document.location.toString()).searchParams;

    fetch(`/${url}/?${params}`, {
        method: `${method}`,
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: JSON.stringify(data)
    }).then((response) => {
        if (response.ok) {
            location.reload();
        } else {
            alert("Невозможно выполнить действие");
        }
    }).catch((error) => {
        console.error("Ошибка сети:", error);
    });
}
