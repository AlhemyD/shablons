from Src.Models.receipt_model import receipt_model
from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model

'''
Класс для запуска сервиса
'''


class start_service:
    __repo: reposity = reposity()

    def __init__(self):
        self.__repo.data[reposity.range_key()] = []
        self.__repo.data[reposity.group_key()] = []
        self.__repo.data[reposity.nomenclature_key()] = []

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    # Метод формирования и сохранения данных по единицам измерения, группам и номенклатурам.
    def __create(self):
        self.__default_create_range()
        self.__default_create_group()
        self.__default_create_nomenclature()

    # Создать эталон единиц измерения
    def __default_create_range(self):
        self.__repo.append(reposity.range_key(), range_model.create_gramm())
        self.__repo.append(reposity.range_key(), range_model.create_kill())

    # Создать эталон групп
    def __default_create_group(self):
        self.__repo.append(reposity.group_key(), group_model())

    # Создать эталон номенклатур
    def __default_create_nomenclature(self):
        self.__repo.append(reposity.nomenclature_key(),
                           nomenclature_model(_group=group_model(_name="Название группы номенклатуры"),
                                              _range=range_model.create_gramm()))

    # Создать эталонные рецепты
    def __create_receipts(self):
        my_receipt = receipt_model()
        another_receipt = receipt_model()

        my_receipt.name = "Гренки с яйцом на сковороде"
        another_receipt.name = "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ"

        my_receipt.number_of_servings = 3
        another_receipt.number_of_servings = 10

        my_receipt.cooking_length = range_model(_name="ч", _value=1)
        another_receipt.cooking_length = range_model(_name="мин", _value=20)

        my_receipt.ingredients = [
            nomenclature_model(
                _group=group_model(_name="Батон"),
                _range=range_model(_name="гр", _value=250)
            ),
            nomenclature_model(
                _group=group_model(_name="Сахар"),
                _range=range_model(_name="гр", _value=25)
            ),
            nomenclature_model(
                _group=group_model(_name="Растительное масло"),
                _range=range_model(_name="гр", _value=20)
            ),
            nomenclature_model(
                _group=group_model(_name="Яйца"),
                _range=range_model(_name="шт", _value=2)
            ),
            nomenclature_model(
                _group=group_model(_name="Молоко"),
                _range=range_model(_name="гр", _value=28)
            )
        ]
        another_receipt.ingredients = [
            nomenclature_model(
                _group=group_model(_name="Пшеничная мука"),
                _range=range_model(_name="гр", _value=100)
            ),
            nomenclature_model(
                _group=group_model(_name="Сахар"),
                _range=range_model(_name="гр", _value=80)
            ),
            nomenclature_model(
                _group=group_model(_name="Сливочное масло"),
                _range=range_model(_name="гр", _value=70)
            ),
            nomenclature_model(
                _group=group_model(_name="Яйца"),
                _range=range_model(_name="шт", _value=1)
            ),
            nomenclature_model(
                _group=group_model(_name="Ванилин(щепотка)"),
                _range=range_model(_name="гр", _value=5)
            )
        ]

        my_receipt.steps = [
            '''Как пожарить гренки с яйцом на сковороде? Подготовьте необходимые ингредиенты. Хлеб лучше использовать немного подсохший, его проще будет нарезать на тонкие ломтики. Количество сахара можно регулировать по своему вкусу. А для любителей несладких гренок можно сахар совсем исключить и яичную смесь немного подсолить. В таком варианте получатся соленые гренки. В глубокую миску вбейте яйца.''',
            '''Добавьте немного сахара.''',
            '''Затем влейте совсем немного, буквально, пару ложек молока. Перемешайте все с помощью венчика или вилки до однородности, чтобы появились небольшие пузырьки. Таким образом, смесь насытится воздухом.''',
            '''Батон нарежьте на ломтики толщиной 1-2 сантиметра.''',
            '''Каждый ломтик батона обмакните в яичную смесь с двух сторон.''',
            '''Сковороду разогрейте до горячего состояния, налейте немного растительного масла и выложите ломтики батона в яичной смеси. Обжаривайте гренки с яйцом и молоком на сковороде с каждой стороны в течение 1-2 минут до аппетитной корочки.''',
            '''Готовые гренки выкладывайте на бумажную салфетку, чтобы удалить с них лишний жир. Угощайтесь вкусными гренками с чаем или кофе. А детям можно предложить к ним молоко или какао. Приятного аппетита!'''
        ]
        another_receipt.steps = [
            '''Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.''',
            '''Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.''',
            '''Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.''',
            '''Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.''',
            '''Всыпьте муку, добавьте ванилин.''',
            '''Перемешайте массу венчиком до состояния гладкого однородного теста.''',
            '''Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.''',
            '''Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик.'''
        ]

        self.__repo.receipts.append(my_receipt)
        self.__repo.receipts.append(another_receipt)

    # Основной метод для генерации эталонных данных
    def start(self):
        self.__create()
        self.__create_receipts()

    # Стартовый набор данных
    def data(self):
        return self.__repo.data

    # Стартовый набор рецептов
    def receipts(self):
        return self.__repo.receipts
