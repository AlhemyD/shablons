class Settings:
    __name:str = ""
    __inn:str = ""
    __acc_number:str = ""
    __corr_acc_number:str = ""
    __bic:str = ""
    __ownership:str = ""

    def __init__(self, value:dict):
        if "name" in value:
            self.__name = value["name"]
        if "inn" in value:
            self.__inn = value["inn"]
        if "acc_number" in value:
            self.__acc_number = value["acc_number"]
        if "corr_acc_number" in value:
            self.__corr_acc_number = value["corr_acc_number"]
        if "bic" in value:
            self.__bic = value["bic"]
        if "ownership" in value:
            self.__ownership = value["ownership"]


    @property
    def name(self) -> str:
        return self.__name
    @name.setter
    def name(self, value:str):
        if value.strip() != "":
            self.__name = value.strip()
        else:
            raise Exception("Company name is empty")

    @property
    def inn(self) -> str:
        return self.__inn
    @inn.setter
    def inn(self, value: str):
        if value.strip() != "" and len(value.strip()) == 12:
            self.__inn = value.strip()
        else:
            raise Exception("Company inn must be of length 12")

    @property
    def acc_number(self) -> str:
        return self.__acc_number
    @acc_number.setter
    def acc_number(self, value: str):
        if value.strip() != "" and len(value.strip()) == 11:
            self.__acc_number = value.strip()
        else:
            raise Exception("Company acc_number must be of length 11")

    @property
    def corr_acc_number(self) -> str:
        return self.__corr_acc_number

    @corr_acc_number.setter
    def corr_acc_number(self, value: str):
        if value.strip() != "" and len(value.strip()) == 11:
            self.__corr_acc_number = value.strip()
        else:
            raise Exception("Company corr_acc_number must be of length 11")

    @property
    def bic(self) -> str:
        return self.__bic

    @bic.setter
    def bic(self, value: str):
        if value.strip() != "" and len(value.strip()) == 9:
            self.__bic = value.strip()
        else:
            raise Exception("Company bic must be of length 9")

    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        if value.strip() != "" and len(value.strip()) == 5:
            self.__ownership = value.strip()
        else:
            raise Exception("Company ownership must be of length 5")