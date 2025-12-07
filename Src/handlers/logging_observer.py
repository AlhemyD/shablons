from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type as EventType
from logging import Logger, StreamHandler, FileHandler, Formatter
import json

from src.core.log_level import LogLevel


class LoggingObserver(abstract_logic):
    def __init__(self, min_level: LogLevel, output: str, start_service):
        super().__init__(start_service)
        self.min_level = min_level
        self.output = output
        self.logger = Logger("SystemLogger")

        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        if output == "console":
            handler = StreamHandler()
        else:
            handler = FileHandler(output)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle(self, event_type: str, payload: dict):
        level_map = {
            EventType.DEBUG_EVENT: LogLevel.DEBUG,
            EventType.INFO_EVENT: LogLevel.INFO,
            EventType.ERROR_EVENT: LogLevel.ERROR
        }

        if level_map.get(event_type, LogLevel.ERROR).value >= self.min_level.value:
            msg = f"Event: {event_type}, Payload: {json.dumps(payload)}"
            if event_type == EventType.DEBUG_EVENT:
                self.logger.debug(msg)
            elif event_type == EventType.INFO_EVENT:
                self.logger.info(msg)
            elif event_type == EventType.ERROR_EVENT:
                self.logger.error(msg)