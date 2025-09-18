class company_model:
    __name:str = ""
    __inn:str = ""

    def _init_(self):
        pass

    @property
    def name(self)->str:
        return self.__name

    @name.setter
    def name(self, value:str):
        if value.strip() != "":
            self.__name = value.strip()

    @property
    def inn(self)->str:
        return self.__inn
