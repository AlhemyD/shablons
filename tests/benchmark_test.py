# Функция для генерации транзакций
from random import random

from src.models.transaction_model import TransactionModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.storage_model import StorageModel
from src.models.measure_unit_model import MeasureUnitModel
from datetime import timedelta, datetime

import random
import time
from datetime import date
from src.logics.osd_tbs import OsdTbs
from src.singletons.repository import Repository
from src.singletons.settings_manager import SettingsManager
from src.singletons.start_service import StartService
from src.models.settings_model import SettingsModel


def generate_transactions(num_transactions):
    transactions = []
    now = datetime.now()
    for i in range(num_transactions):
        # Рандомные даты от прошлого месяца до настоящего времени
        rand_days = random.randint(-30, 0)
        transaction_date = now + timedelta(days=rand_days)

        # Создаем транзакцию
        nomenclature = NomenclatureModel(name=f'Nomenclature_{i}')
        storage = StorageModel(name=f'Storage_{i}')
        measure_unit = MeasureUnitModel.create_gramm()

        transaction = TransactionModel(
            name=f"Transaction_{i}_",
            date=transaction_date,
            nomenclature=nomenclature,
            storage=storage,
            quantity=random.uniform(1, 100),  # случайное количество
            measure_unit=measure_unit
        )
        transactions.append(transaction)
    return transactions



# Генерируем фиксированное количество транзакций
NUM_TRANSACTIONS = 500000
TRANSACTIONS = generate_transactions(NUM_TRANSACTIONS)

# Настройка менеджера настроек
settings_manager = SettingsManager()
settings_manager.settings.block_period = date(2024, 1, 1)

# Создаем объект StartService с нашими транзакциями

start_service = StartService()
start_service.start("data/settings.json")

for i in TRANSACTIONS:

    start_service.data[Repository.transactions_key][i.name] = i


# Массив дат блокировки для замера производительности
BLOCK_DATES = [date(2024, 1, 1), date(2024, 6, 1), date(2024, 10, 1)]

# Основной цикл тестирования
results = []
for block_date in BLOCK_DATES:
    settings_manager.settings.block_period = block_date
    start_time = time.time()
    OsdTbs.calculate_with_block(
        storage_id="Главный склад",
        start=date(2024, 1, 1),
        end=date(2024, 10, 1),
        start_service=start_service,
        settings=settings_manager.settings
    )
    elapsed_time = time.time() - start_time
    results.append((block_date, elapsed_time))

# Печать результатов в Markdown таблице
output = "# Benchmark Results\n\n| Block Date | Execution Time |\n|------------|----------------|\n"
for block_date, exec_time in results:
    output += f"| {block_date} | {exec_time} sec |\n"