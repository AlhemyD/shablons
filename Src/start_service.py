import os
import json
from datetime import datetime

from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Core.validator import validator, argument_exception, operation_exception


class start_service:
    __repo: reposity = reposity()
    __default_receipt: receipt_model
    __cache = {}
    __full_file_name: str = ""

    def __init__(self):
        self.__repo.initalize()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    @property
    def file_name(self) -> str:
        return self.__full_file_name

    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:

                settings = json.load(file_instance)

                if "default_receipt" in settings.keys() and settings.get("first_run"):
                    data = settings["default_receipt"]
                    return self.convert(data)

            return False
        except Exception as e:
            return False

    def __save_item(self, key: str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[key].append(item)

    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data.get('ranges', [])
        if not ranges:
            return False
        for range_ in ranges:
            dto = range_dto().create(range_)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.range_key(), dto, item)
        return True

    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories = data.get('categories', [])
        if not categories:
            return False
        for category in categories:
            dto = category_dto().create(category)
            item = group_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.group_key(), dto, item)
        return True

    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures = data.get('nomenclatures', [])
        if not nomenclatures:
            return False
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.nomenclature_key(), dto, item)
        return True

    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        # Рецепт
        cooking_time = data.get('cooking_time', "")
        portions = int(data.get('portions', 0))
        name = data.get('name', "НЕ ИЗВЕСТНО")
        self.__default_receipt = receipt_model.create(name, cooking_time, portions)

        steps = data.get('steps', [])
        for step in steps:
            if step.strip():
                self.__default_receipt.steps.append(step)

        self.__convert_ranges(data)
        self.__convert_groups(data)
        self.__convert_nomenclatures(data)

        compositions = data.get('composition', [])
        for composition in compositions:
            namnomenclature_id = composition.get('nomenclature_id', "")
            range_id = composition.get('range_id', "")
            value = composition.get('value', 0)
            nomenclature = self.__cache.get(namnomenclature_id)
            range_ = self.__cache.get(range_id)
            item = receipt_item_model.create(nomenclature, range_, value)
            self.__default_receipt.composition.append(item)

        self.__repo.data[reposity.receipt_key()].append(self.__default_receipt)
        return True

    @property
    def data(self):
        return self.__repo.data

    def start(self):
        file_path = os.path.join(os.path.dirname(__file__), "settings.json")
        if not os.path.exists(file_path):
            raise operation_exception(f"Файл настроек не найден: {file_path}")

        self.file_name = file_path
        result = self.load()
        if not result:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")

        self.initialize_storages_and_transactions()

    def get_initial_balance(self, nomenclature_id, date):
        """
        Получает начальный баланс по номенклатуре на указанную дату.
        """
        transactions = self.data[reposity.transaction_key()]
        filtered_transactions = [
            t for t in transactions
            if t.date < datetime.strptime(date, '%Y-%m-%d') and t.nomenclature.unique_code == nomenclature_id
        ]

        balance = sum(t.quantity for t in filtered_transactions)
        return balance

    def initialize_storages_and_transactions(self):
        """
        Добавляет шаблоны склада и транзакции
        """
        # Пример добавления данных для складов
        storage1 = storage_model()
        storage1.address = "Москва, ул. Тверская, д. 1"
        storage1.name = "Склад1"
        storage1.unique_code = "strg1"
        self.data[reposity.storage_key()].append(storage1)

        transaction1 = transaction_model()
        transaction1.date = datetime.now()
        transaction1.nomenclature = nomenclature_model()
        transaction1.nomenclature.name = "Номенклатура1"
        transaction1.nomenclature.group = group_model().create("Группа Номенклатуры1")
        transaction1.nomenclature.range = range_model.create_kill()
        transaction1.storage = storage1
        transaction1.quantity = 100
        transaction1.unit = range_model.create_kill()
        self.data[reposity.transaction_key()].append(transaction1)

        transaction2 = transaction_model()
        transaction2.date = datetime.now()
        transaction2.nomenclature = nomenclature_model()
        transaction2.nomenclature.name = "Номенклатура2"
        transaction2.nomenclature.group = group_model().create("Группа Номенклатуры2")
        transaction2.nomenclature.range = range_model.create_kill()
        transaction2.storage = storage1
        transaction2.quantity = -10
        transaction2.unit = range_model.create_kill()
        self.data[reposity.transaction_key()].append(transaction2)
