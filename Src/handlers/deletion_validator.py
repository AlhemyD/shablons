from src.core.abstract_logic import abstract_logic as AbstractLogic
from src.core.event_type import event_type as EventType
from src.core.exceptions import OperationException
from src.singletons.repository import Repository

class DeletionValidator(AbstractLogic):
    def handle(self, event_type: str, payload: dict):
        super().handle(event_type, payload)
        if event_type == EventType.REMOVED_REFERENCE:
            ref_type = payload.get("ref_type")
            unique_code = payload.get("unique_code")

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

            del self.start_service.repository.data[ref_type][unique_code]