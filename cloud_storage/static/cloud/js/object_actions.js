document.addEventListener("DOMContentLoaded", () => {
    const createFileButton = document.getElementById("create-file-button");
    const createFolderButton = document.getElementById("create-folder-button");

    createFileButton.addEventListener("click", () => {
        name_file = prompt("Введите название объекта:", '');
        if (validate_name(name_file)) {
            create_object(name_file);
        }
    }
    );

    createFolderButton.addEventListener("click", () => {
        name_folder = prompt("Введите название объекта:", '');
        if (validate_name(name_folder)) {
            create_object(name_folder + '/');
        }
    }
    );

    function validate_name(nameObject) {
        if (nameObject && nameObject.trim() !== "" && nameObject.length < 12) {
            return true;
        } else {
            alert("Неверное название объекта");
            return false;
        }
    }

    function create_object(nameObject) {
        let object_info = {
            nameFolder: nameObject
        };

        fetch('/create_object/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(object_info)
        }).then((response) => {
            if (response.ok) {
                location.reload();
            }
        });
    }

    function delete_object(nameObject) {
        let object_info = {
            nameFolder: nameObject
        };

        fetch('/delete_object/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(object_info)
        }).then((response) => {
            if (response.ok) {
                location.reload();
            }
        });
    }
});