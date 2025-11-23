from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.response_format import ResponseFormat
from src.models.company_model import CompanyModel
from typing import Optional, List, Dict
from datetime import date

"""Модель настроек

Инкапсулирует модель компании.
"""
class SettingsModel(AbstractModel):
    # Ссылка на объект модели компании
    __company: CompanyModel = None

    # Формат ответов (по умолчанию JSON)
    __response_format: ResponseFormat

    # Дата блокировки
    __block_period: Optional[date] = None

    # Хранение оборотов до даты блокировки
    __turnover_until_block: Optional[List[Dict]] = None

    def __init__(self):
        super().__init__()
        self.__company = CompanyModel()
        self.__response_format = ResponseFormat.JSON

    @property
    def block_period(self):
        return self.__block_period

    @block_period.setter
    def block_period(self, value):

        self.__block_period = value

    """Поле компании"""
    @property
    def company(self) -> CompanyModel:
        return self.__company
    
    """Поле формата ответов"""
    @property
    def response_format(self) -> ResponseFormat:
        return self.__response_format
    
    @response_format.setter
    def response_format(self, value: ResponseFormat):
        self.__response_format = value

    @property
    def turnover_until_block(self) -> Optional[List[Dict]]:
        return self.__turnover_until_block

    @turnover_until_block.setter
    def turnover_until_block(self, value: Optional[List[Dict]]):
        self.__turnover_until_block = value