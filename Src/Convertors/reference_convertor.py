from Src.Core.abstract_model import abstact_model
from Src.Convertors.abstract_convertor import abstract_converter
from Src.Core.common import common
from Src.Core.validator import validator


class reference_converter(abstract_converter):
    """
    Конвертирует объекты, унаследованные от abstract_model.
    """

    def __init__(self, conv_factory=None):
        self.__conv_factory = conv_factory

    def convert(self, obj: abstact_model):
        validator.validate(obj, abstact_model)
        result = {}
        # Рекурсия для вложенных объектов
        for attr_name in common.get_fields(obj):
            if attr_name.startswith("_"):
                continue

            attr_value = getattr(obj, attr_name)
            if isinstance(attr_value, abstact_model):
                # Используем фабрику для конверсии вложенного объекта
                nested_result = self.__conv_factory.convert_object(attr_value)
                result[attr_name] = nested_result
            else:
                result[attr_name] = attr_value

        return result
