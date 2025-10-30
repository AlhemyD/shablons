from Src.Core.abstract_response import abstract_response
from Src.Convertors.convert_factory import convert_factory
import json



class response_json(abstract_response):
    def build(self, format:str, data: list):
        text = super().build(format, data)
        factory = convert_factory()
        result = []
        for item in data:
            result.append(factory.convert_object(item))
        return json.dumps(result, ensure_ascii=False, indent=2)
