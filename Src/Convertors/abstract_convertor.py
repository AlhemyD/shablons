from abc import ABC, abstractmethod


class abstract_converter(ABC):
    """
    Абстрактный класс для сериализации объектов.
    """

    @abstractmethod
    def convert(self, obj: object):
        """
        Преобразует объект в словарь.
        :param obj: Объект для преобразования.
        :return: Словарь с полями объекта.
        """
        pass