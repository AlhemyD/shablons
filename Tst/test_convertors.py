import unittest
from datetime import datetime
from Src.Convertors.basic_convertor import basic_converter
from Src.Convertors.datetime_convertor import datetime_converter
from Src.Convertors.reference_convertor import reference_converter
from Src.Core.abstract_model import abstact_model

#Набор тестов для конвертаторов
class test_convertors(unittest.TestCase):

    # Проверяем конвертацию строки
    def test_basic_converter_string(self):
        # Подготовка
        converter = basic_converter()
        # Действие
        result = converter.convert("Hello")
        # Проверки
        self.assertEqual(result['value'], "Hello")

    # Проверяем конвертацию числа
    def test_basic_converter_number(self):
        # Подготовка
        converter = basic_converter()
        # Действие
        result = converter.convert(42)
        # Проверки
        self.assertEqual(result['value'], 42)

    # Проверяем конвертацию датавремя
    def test_datetime_conversion(self):
        # Подготовка
        converter = datetime_converter()
        dt = datetime.now()
        # Действие
        result = converter.convert(dt)
        # Проверки
        self.assertIn('value', result)
        self.assertIsInstance(result['value'], str)

    # Проверяем конвертацию референс
    def test_reference_conversion(self):
        # Подготовка
        converter = reference_converter()
        my_obj = abstact_model()
        # Действие
        result = converter.convert(my_obj)
        # Проверки
        self.assertIn('unique_code', result)
