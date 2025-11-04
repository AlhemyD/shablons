from Src.Core.entity_model import entity_model
from datetime import datetime
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator

"""
Модель транзакции
"""


class transaction_model(entity_model):
    __date: datetime
    __nomenclature: nomenclature_model
    __storage: storage_model
    __quantity: int
    __unit: range_model

    """
    Дата транзакции
    """

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        validator.validate(value, datetime)
        self.__date = value

    """
    Номенклатура транзакции
    """

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    """
    Склад транзакции
    """

    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value


    """
    Количество
    """
    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int):
        validator.validate(value, int)
        self.__quantity = value

    """
    Единица измерения
    """
    @property
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        validator.validate(value, range_model)
        self.__unit = value
