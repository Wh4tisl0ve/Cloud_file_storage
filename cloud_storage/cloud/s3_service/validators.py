from .exceptions import ObjectNameError


def check_object_name(object_name: str) -> None:
    if not (object_name and len(object_name) < 40):
        raise ObjectNameError('Неверное имя объекта')
