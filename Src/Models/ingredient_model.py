from Src.Core.entity_model import entity_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator

"""
Модель ингредиента рецепта
"""


class ingredient_model(entity_model):
    __nomenclature: nomenclature_model = nomenclature_model()
    __range: range_model = range_model()

    def __init__(self, _name: str = "", _nomenclature: nomenclature_model = nomenclature_model(),
                 _range: range_model = range_model()):
        super().__init__(_name)
        self.nomenclature = _nomenclature
        self.range = _range

    # Единица измерения в рецепте
    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    # Номенклатура ингредиента
    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value
