from src.models.company_model import company_model
from src.models.Settings import Settings
import os
import json
####################################################3
# Менеджер настроек. 
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager:
    __file_name:str = ""
    __company:company_model = None
    __settings:Settings = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
    
    def __init__(self):
        self.set_default()

    # Параметры организации из настроек
    @property
    def company(self) -> company_model:
        return self.__company

    #Объект класса Settings.py
    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def file_name(self) -> str:
        return self.__file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        if value.strip() == "":
            return
        
        if os.path.exists(value):
            self.__file_name = value.strip()
        else:
            if not os.path.isabs(value):
                value = os.path.abspath(value).replace("\\", "/")
                if os.path.exists(value):
                    self.__file_name=value.strip()
                else:
                    raise Exception("Не найден файл настроек!")


    # Загрузить настройки из Json файла
    def load(self, filename:str = "") -> bool:
        if filename:
            self.file_name = filename
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")

        try:
            with open(self.__file_name.strip(), 'r', encoding='utf-8') as file_instance:
                data = json.load(file_instance)

                if "company" in data.keys():
                    item = data["company"]
                
                    self.__company.name = item["name"]
                    return True

            return False
        except:
            return False

    #Создать объект класса Settings.py
    def convert(self, filename:str="") -> bool:
        if filename:
            self.file_name = filename
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")

        try:
            with open(self.file_name.strip(),'r', encoding='utf-8') as file_instance:
                data = json.load(file_instance)
                if "company" in data:
                    item=data["company"]
                    self.__settings = Settings(item)
                    return True
            return False
        except:
            return False

    # Параметры настроек по умолчанию
    def set_default(self):
        self.__company = company_model()
        self.__company.name = "Рога и копыта"


