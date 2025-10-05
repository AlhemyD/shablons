from Src.settings_manager import settings_manager
from Src.Models.company_model import company_model
import unittest
from Src.Models.storage_model import storage_model
import uuid
from Src.Models.nomenclature_model import nomenclature_model
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Models.range_model import range_model
class test_start(unittest.TestCase):

    __start_service: start_service = start_service()
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    def test_start_service_start_rangeNotEmpty(self):
        #Подготовка

        #Действие

        #Проверка
        assert len(self.__start_service.data()) > 0
        assert range_model.create_kill().base.name == range_model.create_gramm().name
        #assert Киллограмм.БазоваяЕдиница.Код = Грамм.Код