export function create_object(nameObject) {
    const object_info = { nameObject: nameObject };
    send_request('create_object', 'POST', object_info);
}

export function delete_object(nameObject) {
    const object_info = { nameObject: nameObject };
    send_request('delete_object', 'DELETE', object_info);
}

export function rename_object(oldName, newName) {
    const names_data = { oldName: oldName, newName: newName };
    send_request('rename_object', 'PATCH', names_data);
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
