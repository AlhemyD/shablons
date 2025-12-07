import json

from src.core.abstract_logic import abstract_logic


class SettingsChangedHandler(abstract_logic):
    def handle(self, event_type: str, payload: dict):
        super().handle(event_type, payload)
        unique_code = payload.get("unique_code")
        """
            Сохраняет изменения в файле настроек appsettings.json.
        """
        config_file = "data/appsettings.json"
        with open(config_file, "r+") as f:
            config = json.load(f)
            config[event_type] = unique_code
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()