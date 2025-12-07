from src.core.abstract_logic import abstract_logic

"""
Реализация наблюдателя
"""


class observe_service:
    handlers = []

    def __init__(self, start_service):
        self.start_service = start_service

    """
    Добавить объект под наблюдение
    """

    @staticmethod
    def add(instance):
        if instance is None:
            return
        if not isinstance(instance, abstract_logic):
            raise AttributeError("instance should be abstract_logic")

        if instance not in observe_service.handlers:
            observe_service.handlers.append(instance)

    @staticmethod
    def delete(instance):
        if instance is None:
            return
        if not isinstance(instance, abstract_logic):
            raise AttributeError("instance should be abstract_logic")

        if instance in observe_service.handlers:
            observe_service.handlers.remove(instance)

    """
    Вызвать событие
    """

    @staticmethod
    def create_event(event: str, params):
        for instance in observe_service.handlers:
            instance.handle(event, params)
