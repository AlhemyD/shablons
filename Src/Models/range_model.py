from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception

"""
Модель единицы измерения
"""


class range_model(entity_model):
    __value: int = 1
    __base: 'range_model' = None

    def __init__(self, _name: str = "", _value: int = 1, _base: 'range_model' = None):
        super().__init__(_name)
        self.value = _value
        self.base = _base

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

    #Создать единицу измерения килограмм
    @staticmethod
    def create_kill():
        inner_gramm = range_model.create("грамм")
        return range_model.create("кг", inner_gramm)

    #Создать единицу измерения грамм
    @staticmethod
    def create_gramm():
        return range_model.create("грамм")

    #Создать единицу измерения name с базовой единицей измерения base
    @staticmethod
    def create(name: str, base=None):
        if not base is None:
            validator.validate(base, range_model)
        item = range_model()
        item.name = name
        item.base = base
        return item
