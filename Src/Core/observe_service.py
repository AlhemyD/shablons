import json
from datetime import datetime, date

from src.core.abstract_logic import abstract_logic
from src.logics.osd_tbs import OsdTbs
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.core.exceptions import OperationException

"""
Реализация наблюдателя
"""


class observe_service:
    handlers = []

    def __init__(self, start_service: StartService):
        self.start_service = start_service

    """
    Добавить объект под наблюдение
    """

    @staticmethod
    def add(instance):
        if instance is None:
            return
        if not isinstance(instance, abstract_logic):
            return

        if instance not in observe_service.handlers:
            observe_service.handlers.append(instance)

    def after_edit_handler(self, params):
        ref_type = params.get("ref_type")
        unique_code = params.get("unique_code")
        new_value = params.get("new_value")

        if ref_type == "nomenclature":
            recipes_using_nomenclature = [
                r for r in self.start_service.repository.data[Repository.recipes_key].values()
                if any(i.nomenclature.unique_code == unique_code for i in r.ingredients)
            ]
            transaction_using_nomenclature = [
                r for r in self.start_service.repository.data[Repository.transactions_key].values()
                if r.nomenclature.unique_code == unique_code
            ]

            for r in recipes_using_nomenclature:
                for i in r.ingredients:
                    if i.nomenclature.unique_code == unique_code:
                        i.nomenclature = new_value
            for t in transaction_using_nomenclature:
                t.nomenclature = new_value
        elif ref_type == "measure_unit":
            transaction_using_measure = [
                r for r in self.start_service.repository.data[Repository.transactions_key].values()
                if r.measure_unit.unique_code == unique_code
            ]
            recipes_using_measure = [
                r for r in self.start_service.repository.data[Repository.recipes_key].values()
                if any(i.measure_unit.unique_code == unique_code for i in r.ingredients)
            ]
            nomenclatures_using_measure_unit = [
                n for n in self.start_service.repository.data[Repository.nomenclatures_key].values()
                if n.measure_unit.unique_code == unique_code
            ]
            measure_using_measure_unit = [
                n for n in self.start_service.repository.data[Repository.measure_unit_key].values()
                if n.base_unit.unique_code == unique_code
            ]
            for t in transaction_using_measure:
                t.measure_unit = new_value
            for r in recipes_using_measure:
                for i in r.ingredients:
                    if i.measure_unit.unique_code == unique_code:
                        i.measure_unit = new_value
            for n in nomenclatures_using_measure_unit:
                n.measure_unit = new_value
            for m in measure_using_measure_unit:
                m.measure_unit = new_value
        elif ref_type == "nomenclature_group":
            nomenclatures_using_group = [
                n for n in self.start_service.repository.data[Repository.nomenclatures_key].values()
                if n.group.unique_code == unique_code
            ]
            for n in nomenclatures_using_group:
                n.group = new_value
        elif ref_type == "storage":
            transaction_using_storage = [
                n for n in self.start_service.repository.data[Repository.transactions_key].values()
                if n.storage.unique_code == unique_code
            ]
            for t in transaction_using_storage:
                t.storage = new_value
            self.recalculate_stoc(unique_code)
        self.settings_changed_handler({"setting_key":unique_code, "new_value":new_value.unique_code})

    def recalculate_stoc(self, storage_id:str):
        OsdTbs.calculate_with_block(
            storage_id=storage_id,
            start=date(1900, 1, 1),
            end=datetime.now(),
            start_service=self.start_service,
            settings=self.start_service.settings_manager.settings
        )

    def settings_changed_handler(self, params):
        setting_key = params.get("setting_key")
        new_value = params.get("new_value")

        # Сохраняем изменения в файле настроек
        """
            Сохраняет изменения в файле настроек appsettings.json.
            """
        config_file = "data/appsettings.json"
        with open(config_file, "r+") as f:
            config = json.load(f)
            config[setting_key] = new_value
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()

    def before_delete_handler(self, params):
        ref_type = params.get("ref_type")
        unique_code = params.get("unique_code")

        if ref_type == "nomenclature":
            recipes_using_nomenclature = [
                r for r in self.start_service.repository.data[Repository.recipes_key].values()
                if any(i.nomenclature.unique_code == unique_code for i in r.ingredients)
            ]
            transaction_using_nomenclature = [
                r for r in self.start_service.repository.data[Repository.transactions_key].values()
                if r.nomenclature.unique_code == unique_code
            ]
            if recipes_using_nomenclature or transaction_using_nomenclature:
                raise OperationException(
                    f"Невозможно удалить номенклатуру {unique_code}, "
                )

        elif ref_type == "measure_unit":
            transaction_using_measure = [
                r for r in self.start_service.repository.data[Repository.transactions_key].values()
                if r.measure_unit.unique_code == unique_code
            ]
            recipes_using_measure = [
                r for r in self.start_service.repository.data[Repository.recipes_key].values()
                if any(i.measure_unit.unique_code == unique_code for i in r.ingredients)
            ]
            nomenclatures_using_measure_unit = [
                n for n in self.start_service.repository.data[Repository.nomenclatures_key].values()
                if n.measure_unit.unique_code == unique_code
            ]
            measure_using_measure_unit = [
                n for n in self.start_service.repository.data[Repository.measure_unit_key].values()
                if n.base_unit.unique_code == unique_code
            ]
            if nomenclatures_using_measure_unit or measure_using_measure_unit or recipes_using_measure or transaction_using_measure:
                raise OperationException(
                    f"Невозможно удалить единицу измерения {unique_code}, "
                )
        elif ref_type == "nomenclature_group":
            nomenclatures_using_group = [
                n for n in self.start_service.repository.data[Repository.nomenclatures_key].values()
                if n.group.unique_code == unique_code
            ]
            if nomenclatures_using_group:
                raise OperationException(
                    f"Невозможно удалить группу номенклатуры {unique_code}, "
                )
        elif ref_type == "storage":
            transaction_using_storage = [
                n for n in self.start_service.repository.data[Repository.transactions_key].values()
                if n.storage.unique_code == unique_code
            ]
            if transaction_using_storage:
                raise OperationException(
                    f"Невозможно удалить склад {unique_code}, "
                )

    """
    Удалить из под наблюдения
    """

    def delete(self, instance):
        if instance is None:
            return
        if not isinstance(instance, abstract_logic):
            return

        if instance in observe_service.handlers:
            observe_service.handlers.remove(instance)

    """
    Вызвать событие
    """

    @staticmethod
    def create_event(event: str, params):
        for instance in observe_service.handlers:
            instance.handle(event, params)
