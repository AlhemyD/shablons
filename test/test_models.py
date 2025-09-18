from src.models.company_model import company_model

import unittest
class TestModels(unittest.TestCase):
    def test_empty_createmodel_company_model_test(self):

        #Подготовка
        model=company_model()

        #Действие

        #Проверка
        assert model.name == ""

    def test_notEmpty_createmodel_company_model_test(self):
        #Подготовка
        model=company_model()

        #Действие
        model.name="test"

        #Проверка
        assert model.name != ""

if __name__ == '__main__':
    unittest.main()
