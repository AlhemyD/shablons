from typing import Optional
from src.core.abstract_model import AbstractModel
from src.core.event_type import event_type
from src.core.exceptions import OperationException
from src.core.prototype import Prototype


class ReferenceService:
    def __init__(self, start_service):
        self.start_service = start_service
        self.repo = self.start_service.repository
        self.observe_service = self.start_service.observe_service

    def search_reference(self, ref_type: str, unique_code: str) -> Optional[AbstractModel]:
        """
        Осуществляет поиск справочной информации по уникальному коду с использованием прототипа.

        Args:
            ref_type (str): Тип справочника ('nomenclature', 'measure_unit', etc.)
            unique_code (str): Уникальный код объекта

        Returns:
            Optional[AbstractModel]: Найденный объект или None
        """
        proto = Prototype(self.repo.data.get(ref_type, []))
        self.observe_service.create_event(event_type.INFO_EVENT, {"ref_type":ref_type, "unique_code":unique_code})
        return proto.find(lambda x: x.name == unique_code)

    def add_reference(self, ref_type: str, model: AbstractModel) -> bool:
        """
        Добавляет новую справочную информацию в репозиторий.

        Args:
            ref_type (str): Тип справочника
            model (AbstractModel): Объект, который нужно сохранить

        Returns:
            bool: Результат операции
        """
        if self.search_reference(ref_type, model.name):
            self.observe_service.create_event(event_type.ERROR_EVENT, {"ref_type":ref_type, "unique_code":model.unique_code})
            raise OperationException(f"Entity with unique_code={model.name} already exists.")

        self.repo.data.setdefault(ref_type, {})
        self.repo.data[ref_type][model.name] = model
        self.observe_service.create_event(event_type.INFO_EVENT, {"ref_type": ref_type, "unique_code": model.unique_code})
        self.observe_service.create_event(event_type.ADDED_REFERENCE, {"ref_type": ref_type, "model": model})
        return True

    def edit_reference(self, ref_type: str, unique_code: str, model: AbstractModel) -> bool:
        """
        Редактирует существующую справочную информацию.

        Args:
            ref_type (str): Тип справочника
            unique_code (str): Уникальный код объекта
            model (AbstractModel): Модифицированный объект

        Returns:
            bool: Результат операции
        """
        existing_ref = self.search_reference(ref_type, unique_code)
        if not existing_ref:
            self.observe_service.create_event(event_type.ERROR_EVENT,
                                              {"ref_type": ref_type, "unique_code": unique_code, "model_unique_code":model.unique_code})
            raise OperationException(f"Entity with unique_code={unique_code} does not exist.")
        self.observe_service.create_event(event_type.INFO_EVENT,
                                          {"ref_type": ref_type, "unique_code": unique_code, "model_unique_code":model.unique_code})
        self.start_service.observe_service.create_event(event_type.EDITED_REFERENCE, {"ref_type": ref_type, "unique_code":unique_code, "new_value": model})

        return True

    def remove_reference(self, ref_type: str, unique_code: str) -> bool:
        """
        Удаляет справочную информацию по уникальному коду.

        Args:
            ref_type (str): Тип справочника
            unique_code (str): Уникальный код объекта

        Returns:
            bool: Результат операции
        """
        existing_ref = self.search_reference(ref_type, unique_code)
        if not existing_ref:
            self.observe_service.create_event(event_type.ERROR_EVENT,
                                              {"ref_type": ref_type, "unique_code": unique_code})
            raise OperationException(f"Entity with unique_code={unique_code} does not exist.")
        self.observe_service.create_event(event_type.INFO_EVENT,
                                          {"ref_type": ref_type, "unique_code": unique_code})
        self.observe_service.create_event(event_type.REMOVED_REFERENCE, {"ref_type": ref_type, "unique_code": unique_code})
        return True
