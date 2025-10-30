import json
import unittest
from datetime import datetime
from Src.Convertors.convert_factory import convert_factory
from Src.Core.abstract_model import abstact_model
from Src.Models.range_model import range_model


# Модульный тест для фабрики

class test_convert_factory(unittest.TestCase):
    factory = convert_factory()

    # Проверка рекурсивной конверсии
    def test_recursive_conversion(self):
        # Подготовка
        inner_range = range_model()
        inner_range.name = "Inner Range"

        outer_range = range_model()
        outer_range.name = "Outer Range"
        outer_range.base = inner_range

        expected_keys = ['unique_code','name', 'base']

        # Действие
        result = self.factory.serialize_to_json(outer_range)

        # Проверки
        self.assertTrue(all(key in result for key in expected_keys))
        self.assertIsNotNone(result["base"]["unique_code"])
        self.assertEqual(result['base']['name'], "Inner Range")

    # Проверка простых типов конверсии
    def test_simple_types_conversion(self):
        # Подготовка
        simple_value = "Test String"
        # Действие
        result = self.factory.serialize_to_json(simple_value)

        # Проверки
        self.assertEqual(result, {"value": "Test String"})

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
