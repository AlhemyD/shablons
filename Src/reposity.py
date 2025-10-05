from Src.Core.validator import validator
from Src.Models.range_model import range_model
from Src.Core.entity_model import entity_model
from Src.Models.receipt_model import receipt_model
class reposity:
    '''
    Репозиторий данных
    '''
    __data = {}
    __receipts:list[receipt_model] = []

    #Список рецептов
    @property
    def receipts(self):
        return self.__receipts

    #Репозиторий данных
    @property
    def data(self):
        return self.__data

    # Ключ для единиц измерения
    @staticmethod
    def range_key():
        return "range_model"

    # Ключ для групп
    @staticmethod
    def group_key():
        return "group_model"

    # Ключ для номенклатур
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"

    # Метод сохранения данных в __data по ключу key
    def append(self, key: str, value: entity_model):
        validator.validate(value, entity_model)
        validator.validate(key,str)
        if not key in self.data:
            self.data[key] = [value]
        else:
            self.data[key].append(value)