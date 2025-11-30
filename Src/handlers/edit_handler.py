from datetime import datetime, date

from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type
from src.logics.osd_tbs import OsdTbs
from src.singletons.repository import Repository


class EditHandler(abstract_logic):
    def handle(self, _event_type: str, payload: dict):
        super().handle(_event_type, payload)
        if _event_type == event_type.EDITED_REFERENCE:
            ref_type = payload.get("ref_type")
            unique_code = payload.get("unique_code")
            new_value = payload.get("new_value")

            self.start_service.repository.data[ref_type][unique_code] = new_value

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
    def recalculate_stoc(self, storage_id:str):
        OsdTbs.calculate_with_block(
            storage_id=storage_id,
            start=date(1900, 1, 1),
            end=datetime.now(),
            start_service=self.start_service,
            settings=self.start_service.settings_manager.settings
        )