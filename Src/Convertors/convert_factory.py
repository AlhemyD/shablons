from Src.Convertors.basic_convertor import basic_converter
from Src.Convertors.datetime_convertor import datetime_converter
from Src.Convertors.reference_convertor import reference_converter
import json

class convert_factory:
    """
    Фабрика для выбора подходящего конвертера.
    """

    def __init__(self):
        self._converters = [
            basic_converter(),
            datetime_converter(),
            reference_converter(self)
        ]

    def get_converter(self, obj):
        for conv in self._converters:
            try:
                conv.convert(obj)
                return conv
            except Exception:
                pass
        raise ValueError("Не удалось подобрать конвертер для объекта.")

    def convert_object(self, obj):
        converter = self.get_converter(obj)
        return converter.convert(obj)

    def serialize_to_json(self, obj):
        """
        Метод сериализует объект в JSON с использованием наших конвертеров.
        """
        serialized_obj = self.convert_object(obj)
        return serialized_obj