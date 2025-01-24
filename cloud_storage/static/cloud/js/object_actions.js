document.addEventListener("DOMContentLoaded", () => {
    const createObjectButton = document.getElementById("create-object-button");

    createObjectButton.addEventListener("click", () => {
        const nameObject = prompt("Введите название объекта:");

        if (nameObject && nameObject.trim() !== "") {
            create_object(nameObject);
        } else {
            alert("Название объекта не может быть пустым.");
        }
    });


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
        });
    }
});