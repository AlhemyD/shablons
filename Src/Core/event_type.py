"""
Типы событий
"""


class event_type:
    ADDED_REFERENCE = "ADDED_REFERENCE"
    EDITED_REFERENCE = "EDITED_REFERENCE"
    REMOVED_REFERENCE = "REMOVED_REFERENCE"
    UPDATED_SETTINGS = "UPDATED_SETTINGS"
    INTENT_TO_REMOVE_REFERENCE = "INTENT_TO_REMOVE_REFERENCE"

    DEBUG_EVENT = "DEBUG_EVENT"
    INFO_EVENT = "INFO_EVENT"
    ERROR_EVENT = "ERROR_EVENT"

    """
    Событие - смена даты блокировки
    """

    @staticmethod
    def change_block_period() -> str:
        return "change_block_period"

    """
    Событие - сформирован Json
    """

    @staticmethod
    def convert_to_json() -> str:
        return "convert_to_json"

    """
    Получить список всех событий
    """

    @staticmethod
    def events() -> list:
        result = []
        methods = [method for method in dir(event_type) if
                   callable(getattr(event_type, method)) and not method.startswith('__') and method != "events"]
        for method in methods:
            key = getattr(event_type, method)()
            result.append(key)
        result.append(event_type.ADDED_REFERENCE)
        result.append(event_type.REMOVED_REFERENCE)
        result.append(event_type.INTENT_TO_REMOVE_REFERENCE)
        result.append(event_type.EDITED_REFERENCE)
        result.append(event_type.UPDATED_SETTINGS)
        result.append(event_type.DEBUG_EVENT)
        result.append(event_type.INFO_EVENT)
        result.append(event_type.ERROR_EVENT)
        return result
