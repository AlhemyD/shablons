from Src.settings_manager import settings_manager
from Src.Models.company_model import company_model
import unittest
from Src.Models.storage_model import storage_model
import uuid
from Src.Models.nomenclature_model import nomenclature_model
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.range_model import range_model

'''
Тестирование класса start_service
'''


class test_start(unittest.TestCase):
    __start_service: start_service = start_service()

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    # Проверка на создание эталонных данных
    def test_start_service_start_rangeNotEmpty(self):
        # Подготовка

        # Действие

        # Проверка
        assert len(self.__start_service.data()) > 0
        assert len(self.__start_service.data()[reposity.group_key()]) > 0
        assert len(self.__start_service.data()[reposity.nomenclature_key()]) > 0
        assert len(self.__start_service.data()[reposity.range_key()]) > 0
        assert range_model.create_kill().base.name == range_model.create_gramm().name
        assert len(self.__start_service.receipts()) > 0

    # Тестирование на уникальность элементов receipts
    def test_receipt_unique_element(self):
        # Подготовка
        receipts = self.__start_service.receipts()
        unique_receipts = set()

        # Действие
        for receipt in receipts:
            unique_receipts.add(receipt.unique_code)

        # Проверки
        assert len(unique_receipts) == len(receipts)

    # Тестирование на уникальность элементов data[range_model]
    def test_data_range_unique_element(self):
        # Подготовка
        data = self.__start_service.data()
        unique_elements = set()

        # Действие
        for datum in data[reposity.range_key()]:
            unique_elements.add(datum.unique_code)

        # Проверки
        assert len(unique_elements) == len(data[reposity.range_key()])

    # Тестирование на уникальность элементов data[nomenclature_model]
    def test_data_nomenclature_unique_element(self):
        # Подготовка
        data = self.__start_service.data()
        unique_elements = set()

        # Действие
        for datum in data[reposity.nomenclature_key()]:
            unique_elements.add(datum.unique_code)

        # Проверки
        assert len(unique_elements) == len(data[reposity.nomenclature_key()])

    # Тестирование на уникальность элементов data[group_model]
    def test_data_group_unique_element(self):
        # Подготовка
        data = self.__start_service.data()
        unique_elements = set()

        # Действие
        for datum in data[reposity.group_key()]:
            unique_elements.add(datum.unique_code)

        # Проверки
        assert len(unique_elements) == len(data[reposity.group_key()])