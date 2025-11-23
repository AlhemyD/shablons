import unittest
from src.logics.osd_tbs import OsdTbs
from src.models.settings_model import SettingsModel
from src.singletons.settings_manager import SettingsManager
from datetime import date

from src.singletons.start_service import StartService

"""
Модульный тест для проверки правильности расчетов
"""


class TestOsdTbs(unittest.TestCase):
    def setUp(self):
        # Настройка реальных объектов
        self.settings = SettingsModel()
        self.settings.block_period = date(2024, 1, 1)
        self.settings.turnover_until_block = [
            {'unique_code': 'A', 'amount': 10},
            {'unique_code': 'B', 'amount': 20}
        ]

        self.start_service = StartService()
        self.start_service.start("data/settings.json")

    def test_calculation_consistency(self):
        # Подготовка
        # Действие
        # Первые результаты расчета
        first_result = OsdTbs.calculate_with_block(
            storage_id="Главный склад",
            start=date(2024, 1, 1),
            end=date(2024, 10, 1),
            start_service=self.start_service,
            settings=self.settings
        )

        # Повторяем расчет для проверки устойчивости результата
        second_result = OsdTbs.calculate_with_block(
            storage_id="Главный склад",
            start=date(2024, 1, 1),
            end=date(2024, 10, 1),
            start_service=self.start_service,
            settings=self.settings
        )
        # Проверки
        assert first_result == second_result, "Результаты первого и второго расчета различаются!"

