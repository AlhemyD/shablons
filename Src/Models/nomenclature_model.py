from Src.Core.entity_model import entity_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator

"""
Модель номенклатуры
"""


class nomenclature_model(entity_model):
    __group: group_model = group_model()
    __range: range_model = range_model()

    def __init__(self, _name: str = "", _group: group_model = group_model(), _range: range_model = range_model()):
        super().__init__(_name)
        self.group = _group
        self.range = _range

    """
    Группа номенклатуры
    """

    @property
    def group(self) -> group_model:
        return self.__group

    @group.setter
    def group(self, value: group_model):
        validator.validate(value, group_model)
        self.__group = value

    """
    Единица измерения
    """

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value
