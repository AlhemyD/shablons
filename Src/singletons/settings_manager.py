import json
from datetime import date, datetime

from src.core.event_type import event_type
from src.core.validator import Validator as vld
from src.models.settings_model import SettingsModel
from src.logics.osd_tbs import OsdTbs

"""Менеджер настроек

Предназначен для управления настройками и хранения параметров приложения.
"""


class SettingsManager:
    # Ссылка на экземпляр SettingsManager
    __instance = None

    # Абсолютный путь до файла с загруженными настройками
    __file_name: str = ""

    # Инкупсулирумый объект настроек
    __settings: SettingsModel

    __start_service = None

    def __init__(self,start_service=None, block_period=datetime.now()):
        self.__start_service = start_service
        self.default()
        self.__settings.block_period = block_period
        # Добавляем расчет оборотов до даты блокировки
        self.update_turnovers_until_block()

    @property
    def start_service(self):
        return self.__start_service

    @start_service.setter
    def start_service(self, value):
        self.__start_service = value

    def update_turnovers_until_block(self):
        start_service = self.start_service
        turnovers = OsdTbs.calculate_until_block(
            storage_id="Главный склад",
            block_period=self.settings.block_period,
            start_service=start_service
        )
        self.settings.turnover_until_block = turnovers

    """Абсолютный путь к файлу с настройками"""

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        self.start_service.observe_service.create_event(event_type.INFO_EVENT, {"settings_filename":value})
        self.__file_name = vld.is_file_exists(value)

    """Настройки с хранящейся моделью компании"""

    @property
    def settings(self) -> SettingsModel:
        return self.__settings

    @settings.setter
    def settings(self, value: SettingsModel):
        vld.validate(value, SettingsModel, "settings")
        self.__settings = value

    """Метод загрузки файла настроек"""

    def load(self, file_name: str) -> bool:
        self.file_name = file_name
        try:
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                settings = json.load(file)
                self.convert_company_data(settings["company"])
                self.convert_response_format(settings["default_response_format"])

                # Проверяем, нужно ли загружать данные при первом старте
                if settings.get("first_start", False):
                    pass
                self.start_service.observe_service.create_event(event_type.INFO_EVENT, {"settings_loaded": True})
                return True
        except Exception as e:
            self.start_service.observe_service.create_event(event_type.ERROR_EVENT, {"settings_loaded": False})
            return False

    """Метод извлечения данных компании из загуженного файла настроек"""

    def convert_company_data(self, data: dict) -> bool:
        vld.is_dict(data, "data")

        # Поля модели компании, которые могут быть заполнены
        company_model_fields = [
            field for field in dir(self.settings.company)
            if not field.startswith("_")
        ]
        # Ключи загруженного объекта настроек
        matching_keys = [
            key for key in data.keys()
            if key in company_model_fields
        ]

        try:
            for key in matching_keys:
                setattr(self.settings.company, key, data[key])
            return True
        except:
            return False

    """Метод загрузки формата ответов по умолчанию из файла настроек"""

    def convert_response_format(self, data: str) -> bool:
        from src.logics.factory_entities import FactoryEntities
        try:
            format = FactoryEntities.match_formats[data]
            self.settings.response_format = format
            return True
        except KeyError:
            return False

    """Метод инициализации стандартных значений полей"""

    def default(self):
        self.settings = SettingsModel()
        self.settings.company.name = "Default Name"
        self.settings.company.ownership = "owner"
