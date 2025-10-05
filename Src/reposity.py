from Src.Core.validator import validator
from Src.Models.range_model import range_model
class reposity:
    '''
    Репозиторий данных
    '''
    __data = {}

    @property
    def data(self):
        return self.__data

    # Ключ для единиц измерения
    @staticmethod
    def range_key():
        return "range_model"

    def append(self, key: str, value: range_model):
        validator.validate(value, range_model)
        validator.validate(key,str)
        if not key in self.data:
            self.data[key] = [value]
        else:
            self.data[key].append(value)