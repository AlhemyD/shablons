from Src.Convertors.abstract_convertor import abstract_converter
from Src.Core.validator import validator, argument_exception


class basic_converter(abstract_converter):
    """
    Конвертирует примитивные объекты (строки, числа).
    """

    def convert(self, obj: [str, int, float]):
        for _type in [str, int, float]:
            try:
                if validator.validate(obj, _type):
                    return {'value': obj}
            except:
                continue
        raise argument_exception("Given non numeric of string type to convertor")
