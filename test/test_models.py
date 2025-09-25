from src.settings_manager import settings_manager
from src.models.company_model import company_model
import unittest


class test_models(unittest.TestCase):

    # Провери создание основной модели
    # Данные после создания должны быть пустыми
    def test_empty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие

        # Проверки
        assert model.name == ""


    # Проверить создание основной модели
    # Данные меняем. Данные должны быть
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()
        
        # Действие
        model.name = "test"
        
        # Проверки
        assert model.name != ""

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_createmodel_companymodel(self):
        # Подготовка
       file_name = "/jsons/settings.json"
       manager = settings_manager()
       manager.file_name = file_name
       
       # Дейсвтие
       result = manager.load()
            
       # Проверки
       assert result == True

    #Проверка загрузки файла настроек из любого каталога и с любым названием
    def test_load_anyfile(self):
        file_name = "C:/Users/Alhem/shablons/_legacy/hello_company.json"
        manager = settings_manager()
        result = manager.load(file_name)

        assert result == True


    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = "/jsons/settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()


        # Дейсвтие
        manager1.load()

        # Проверки
        assert manager1.company == manager2.company

    #Проверка на загрузку в Settings.py
    def test_convert_settings(self):
        file_name = "C:/Users/Alhem/shablons/jsons/settings.json"
        manager = settings_manager()

        result = manager.convert(file_name)

        assert result == True

        settings = manager.settings

    #Проверка загрузки всех свойств в Settings.py
    def test_settings_convert_all(self):
        file_name= "C:/Users/Alhem/shablons/jsons/settings.json"
        manager=settings_manager()

        result = manager.convert(file_name)
        settings = manager.settings

        assert settings.name == "Рога и копыта"
        assert settings.inn == "123456789011"
        assert settings.acc_number == "12345678901"
        assert settings.corr_acc_number == "12345678901"
        assert settings.bic == "123456789"
        assert settings.ownership == "12345"

    #Проверка загрузки по относительному пути
    def test_relative_load(self):
        file_name = "../jsons/settings.json"
        manager = settings_manager()
        result = manager.load(file_name)
        assert result == True

    #Проверка загрузки по названию файла
    def test_name_load(self):
        file_name = "settings.json"
        manager = settings_manager()
        result = manager.load(file_name)
        assert result == True

    #Проверка загрузки из любой директории
    def test_any_dir_name_load(self):
        file_name = "../halo.json"
        manager = settings_manager()
        result = manager.load(file_name)
        assert result == True


  
if __name__ == '__main__':
    unittest.main()
