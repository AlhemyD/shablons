from datetime import datetime
from Src.Convertors.abstract_convertor import abstract_converter
from Src.Core.validator import validator


class datetime_converter(abstract_converter):
    """
    Конвертирует объект datetime в строку формата ISO.
    """

    def convert(self, obj: datetime):
        validator.validate(obj, datetime)
        return {'value': obj.isoformat()}
