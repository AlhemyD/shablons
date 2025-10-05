from Src.Core.abstract_model import abstact_model
from abc import ABC
from Src.Core.validator import validator

"""
Общий класс для наследования. Содержит стандартное определение: код, наименование
"""


class entity_model(abstact_model):
    __name: str = ""

    def __init__(self, _name: str = ""):
        super().__init__()
        if _name != "":
            self.name = _name

    # Наименование
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        validator.validate(value, str)
        self.__name = value.strip()
