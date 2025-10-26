from Src.Core.abstract_model import abstact_model
from Src.Convertors.abstract_convertor import abstract_converter
from Src.Core.validator import validator


class reference_converter(abstract_converter):
    """
    Конвертирует объекты, унаследованные от abstract_model.
    """

    def convert(self, obj: abstact_model):
        validator.validate(obj, abstact_model)
        return {
            'unique_code': obj.unique_code
        }