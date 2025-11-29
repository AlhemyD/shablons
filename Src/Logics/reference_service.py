from typing import Optional
from src.core.abstract_model import AbstractModel
from src.core.exceptions import OperationException
from src.core.prototype import Prototype
from src.singletons.repository import Repository
from src.singletons.start_service import StartService


class ReferenceService:
    def __init__(self, start_service: StartService):
        self.start_service = start_service
        self.repo = self.start_service.repository

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
            raise OperationException(f"Entity with unique_code={model.name} already exists.")

        self.repo.data.setdefault(ref_type, {})
        self.repo.data[ref_type][model.name] = model
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
            raise OperationException(f"Entity with unique_code={unique_code} does not exist.")
        self.repo.data[ref_type][model.name] = model
        self.start_service.observe_service.after_edit_handler({"ref_type": ref_type, "unique_code": unique_code, "new_value": model})

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
            raise OperationException(f"Entity with unique_code={unique_code} does not exist.")
        self.start_service.observe_service.before_delete_handler({"ref_type":ref_type, "unique_code":unique_code})
        del self.repo.data[ref_type][existing_ref.name]
        return True