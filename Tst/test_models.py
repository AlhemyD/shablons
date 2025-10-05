from Src.settings_manager import settings_manager
from Src.Models.company_model import company_model
import unittest
from Src.Models.storage_model import storage_model
import uuid
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.receipt_model import receipt_model

'''
Тестирование моделей
'''


class test_models(unittest.TestCase):

    # Проверки создания основной модели
    # Данные после создания должны быть пустыми
    def test_empty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие

        # Проверки
        assert model.name == ""

    # Проверить создание основной модели
    # Данные меняем. Данные должны быть
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "settings.json"
        manager = settings_manager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        print(manager.file_name)
        assert result == True

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = "settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()
        check_inn = 123456789

        # Действие
        manager1.load()

        # Проверки
        assert manager1.settings == manager2.settings
        print(manager1.file_name)
        assert (manager1.settings.company.inn == check_inn)
        print(f"ИНН {manager1.settings.company.inn}")

    # Проверка на сравнение двух по значению одинаковых моделей
    def test_equals_storage_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = storage_model()
        storage1.unique_code = id
        storage2 = storage_model()
        storage2.unique_code = id

        # Действие 

        # Проверки
        assert storage1 == storage2

    # Проверить создание номенклатуры и присвоение уникального кода
    def test_equals_nomenclature_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        item1 = nomenclature_model()
        item2 = nomenclature_model()

        # Действие
        item1.unique_code = id
        item2.unique_code = id

        # Проверки
        assert item1 == item2

    # Проверка создания номенклатуры и наличия данных
    def test_nomenclature_model_create(self):
        # Подготовка
        item1 = nomenclature_model(_name="item1", _group=group_model(_name="123"), _range=range_model(_name="грамм"))

        # Действие

        # Проверки
        assert item1.name != ""
        assert item1.group.name == "123"
        assert item1.range.name == "грамм"

    # Проверить создание группы и наличия данных
    def test_group_model_create(self):
        # Подготовка
        group = group_model(_name="Название группы")

        # Действие

        # Проверки
        assert group.name != ""

    # Проверить создание единицы измерения и наличия данных
    def test_range_model_create(self):
        # Подготовка
        range = range_model(_name="килограмм", _value=40, _base=range_model(_name="грамм"))

        # Действие

        # Проверки
        assert range.name != ""
        assert range.value == 40
        assert range.base.name != ""

    # Проверить создание рецепта и наличия данных
    def test_receipt_create(self):
        # Подготовка
        receipt = receipt_model()

        # Действие
        receipt.name = "Гренки с яйцом на сковороде"
        receipt.number_of_servings = 3
        receipt.cooking_length = range_model(_name="ч", _value=1)
        receipt.ingredients = [
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
        receipt.steps = [
            '''Как пожарить гренки с яйцом на сковороде? Подготовьте необходимые ингредиенты. Хлеб лучше использовать немного подсохший, его проще будет нарезать на тонкие ломтики. Количество сахара можно регулировать по своему вкусу. А для любителей несладких гренок можно сахар совсем исключить и яичную смесь немного подсолить. В таком варианте получатся соленые гренки. В глубокую миску вбейте яйца.''',
            '''Добавьте немного сахара.''',
            '''Затем влейте совсем немного, буквально, пару ложек молока. Перемешайте все с помощью венчика или вилки до однородности, чтобы появились небольшие пузырьки. Таким образом, смесь насытится воздухом.''',
            '''Батон нарежьте на ломтики толщиной 1-2 сантиметра.''',
            '''Каждый ломтик батона обмакните в яичную смесь с двух сторон.''',
            '''Сковороду разогрейте до горячего состояния, налейте немного растительного масла и выложите ломтики батона в яичной смеси. Обжаривайте гренки с яйцом и молоком на сковороде с каждой стороны в течение 1-2 минут до аппетитной корочки.''',
            '''Готовые гренки выкладывайте на бумажную салфетку, чтобы удалить с них лишний жир. Угощайтесь вкусными гренками с чаем или кофе. А детям можно предложить к ним молоко или какао. Приятного аппетита!'''
        ]

        # Проверки
        assert receipt.name != ""
        assert receipt.number_of_servings == 3
        assert receipt.cooking_length.name != ""
        assert len(receipt.ingredients) > 0
        assert len(receipt.steps) > 0


if __name__ == '__main__':
    unittest.main()
