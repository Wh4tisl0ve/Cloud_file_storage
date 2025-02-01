from .exceptions import ObjectNameError


def check_object_name(object_name: str) -> None:
    if not (object_name and len(object_name) < 15):
        raise ObjectNameError('Неверное имя объекта')
