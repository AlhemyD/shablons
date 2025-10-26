import unittest
from datetime import datetime
from Src.Convertors.convert_factory import convert_factory
from Src.Core.abstract_model import abstact_model


# Модульный тест для фабрики

class test_convert_factory(unittest.TestCase):
    factory = convert_factory()

    # Проверка convert_factory на выбор правильного конвертора для basic
    def test_factory_selects_proper_converter_basic(self):
        # Подготовка
        # Действие
        result_str = self.factory.convert_object("Hello World!")
        result_int = self.factory.convert_object(42)
        # Проверки
        self.assertEqual(result_str['value'], "Hello World!")
        self.assertEqual(result_int['value'], 42)

    # Проверка convert_factory на выбор правильного конвертора для датавремя
    def test_factory_selects_proper_converter_datetime(self):
        # Подготовка
        # Действие
        result_dt = self.factory.convert_object(datetime.now())
        # Проверки
        self.assertIn('value', result_dt)

    # Проверка convert_factory на выбор правильного конвертора для референс
    def test_factory_selects_proper_converter_reference(self):
        # Подготовка
        my_obj = abstact_model()
        # Действие
        result_ref = self.factory.convert_object(my_obj)
        # Проверки
        self.assertIn('unique_code', result_ref)
