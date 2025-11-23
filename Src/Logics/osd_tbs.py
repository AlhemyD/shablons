from typing import List, Dict
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.logics.tbs_line import TbsLine
from src.models.settings_model import SettingsModel
from src.models.storage_model import StorageModel
from src.models.transaction_model import TransactionModel
from src.models.nomenclature_model import NomenclatureModel
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.logics.prototype_report import PrototypeReport
from src.dtos.filter_dto import FiltredDto
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.core.filter_operators import filter_operators

"""Класс для расчёта оборотно-сальдовой ведомости"""


class OsdTbs:

    @staticmethod
    def calculate_with_block(
            storage_id: str,
            start: date,
            end: date,
            start_service: StartService,
            settings: SettingsModel
    ) -> List[TbsLine]:
        # Сначала используем предыдущие расчеты до даты блокировки
        previous_turnovers = settings.turnover_until_block

        # Затем добавляем новые обороты начиная с даты блокировки
        block_period = settings.block_period
        headers, current_turnovers = OsdTbs.calculate(storage_id, start, block_period, start_service)

        # Группировка и объединение результатов
        result = []
        seen_codes = set()

        # Предварительно собранные обороты
        for entry in previous_turnovers:
            result.append(entry)
            seen_codes.add(entry.get('unique_code'))

        # Новый расчет добавляется, только если запись новая
        for entry in current_turnovers:
            unique_code = entry.get('unique_code')
            if unique_code and unique_code not in seen_codes:
                result.append(entry)
                seen_codes.add(unique_code)

        return result

    @staticmethod
    def calculate_until_block(
            storage_id: str,
            block_period: date,
            start_service: StartService
    ) -> List[TbsLine]:
        """
        Рассчитывает обороты до даты блокировки включительно.

        :param storage_id: Уникальный идентификатор склада
        :param block_period: Дата блокировки
        :param start_service: Экземпляр стартового сервиса
        :return: Список строк TbsLine до даты блокировки
        """
        # Период с самого начала учета до даты блокировки
        start = datetime(1900, 1, 1)
        end = datetime(block_period.year, block_period.month, block_period.day, 23, 59, 59)

        # Получаем нужные транзакции и выполняем стандартный расчёт
        headers, display_data_rows = OsdTbs.calculate(storage_id, start, end, start_service)
        return display_data_rows


    @staticmethod
    def calculate(
            storage_id: str,
            start: date,
            end: date,
            start_service: StartService,
            filters: filter_sorting_dto = None,

    ) -> List[TbsLine]:

        start = datetime(start.year, start.month, start.day)
        end = datetime(end.year, end.month, end.day, 23, 59, 59)
        transactions = list(start_service.transactions.values())
        prototype = PrototypeReport(transactions)
        filt = FiltredDto()
        storage = start_service.repository.get(unique_code=storage_id)
        data = {
            "field_name": "storage",
            "value": storage_id,
            "operator": filter_operators.like(),
        }
        filt.load(data)
        filtered_transactions = prototype.filter(prototype, filt)
        if filters and filters.filters:
            for filter in filters.filters:
                filt = FiltredDto()
                filt.load(filter)
                filter["value"] = start_service.repository.get(unique_code=filter["value"])
                filtered_transactions = prototype.filter(filtered_transactions, filt)

        data: Dict[str, TbsLine] = dict()
        for transaction in filtered_transactions.data:
            code = transaction.nomenclature.unique_code
            if code not in data:
                data[code] = TbsLine(transaction)
                line = data[code]
                line.add(transaction, start, end)

        tbs_keys = data.keys()
        all_keys = StartService().data[Repository.nomenclatures_key].keys()
        other_keys = set(all_keys) - set(tbs_keys)

        for key in other_keys:
            nomenclature = StartService().repository.get(unique_code=key)
            if nomenclature is None:
                continue
            data[key] = TbsLine(TransactionModel(
                nomenclature=nomenclature,
                storage=storage,
                count=0,
                measure_unit=nomenclature.measure_unit
            ))
        tbs_lines: TbsLine = list(data.values())

        headers = TbsLine.get_display_headers()
        display_data_rows = [line.to_display_data() for line in tbs_lines]

        return headers, display_data_rows
