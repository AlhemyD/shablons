from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception

"""
Модель единицы измерения
"""
class range_model(entity_model):
    __value:int = 1
    __base:'range_model' = None

    """
    Значение коэффициента пересчета
    """
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        if value <= 0:
             raise argument_exception("Некорректный аргумент!")
        self.__value = value


    """
    Базовая единица измерения
    """
    @property
    def base(self):
        return self.__base
    
    @base.setter
    def base(self, value):
        self.__base = value

    @staticmethod
    def create_kill():
        inner_gramm = range_model.create("грамм")
        return range_model.create("кг", inner_gramm)

    @staticmethod
    def create_gramm():
        return range_model.create("грамм")

    @staticmethod
    def create(name: str, base=None):
        if not base is None:
            validator.validate(base, range_model)
        item = range_model()
        item.name = name
        item.base = base
        return item
