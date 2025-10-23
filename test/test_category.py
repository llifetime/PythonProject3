import pytest
from io import StringIO
import sys
from src.category import Category
from src.product import Product, Smartphone, LawnGrass


class TestCategoryProductProtection:
    """Тесты защиты от добавления неправильных типов в категорию"""

    def test_add_product_valid_types(self):
        """Тест добавления допустимых типов продуктов"""
        category = Category("Тестовая категория", "Описание категории")
        product = Product("Тестовый продукт", 100.0, 5, "Описание продукта")

        # Должно работать без ошибок
        category.add_product(product)
        assert len(category.products) == 1

    def test_add_product_invalid_string(self):
        """Тест попытки добавления строки"""
        category = Category("Тестовая категория", "Описание категории")

        with pytest.raises(TypeError, match="Можно добавлять только объекты, которые являются продуктами"):
            category.add_product("не продукт")

    def test_add_product_invalid_number(self):
        """Тест попытки добавления числа"""
        category = Category("Тестовая категория", "Описание категории")

        with pytest.raises(TypeError, match="Можно добавлять только объекты, которые являются продуктами"):
            category.add_product(123)

    def test_add_product_invalid_list(self):
        """Тест попытки добавления списка"""
        category = Category("Тестовая категория", "Описание категории")

        with pytest.raises(TypeError, match="Можно добавлять только объекты, которые являются продуктами"):
            category.add_product([1, 2, 3])

    def test_add_product_invalid_dict(self):
        """Тест попытки добавления словаря"""
        category = Category("Тестовая категория", "Описание категории")

        with pytest.raises(TypeError, match="Можно добавлять только объекты, которые являются продуктами"):
            category.add_product({"key": "value"})

    def test_add_product_invalid_none(self):
        """Тест попытки добавления None"""
        category = Category("Тестовая категория", "Описание категории")

        with pytest.raises(TypeError, match="Можно добавлять только объекты, которые являются продуктами"):
            category.add_product(None)

    def test_add_product_mixed_valid_invalid(self):
        """Тест смешанного добавления допустимых и недопустимых объектов"""
        category = Category("Тестовая категория", "Описание категории")
        valid_product = Product("Валидный продукт", 100.0, 5, "Описание")

        # Добавляем валидный продукт
        category.add_product(valid_product)
        assert len(category.products) == 1

        # Пытаемся добавить невалидный
        with pytest.raises(TypeError):
            category.add_product("не продукт")

        # Проверяем, что валидный продукт остался
        assert len(category.products) == 1

    def test_add_product_inheritance_works(self):
        """Тест что наследование работает корректно"""
        category = Category("Тестовая категория", "Описание категории")

        # Проверяем, что наследники Product тоже работают
        smartphone = Smartphone("Смартфон", 500.0, 10, "Model X", 128, "Black")
        lawn_grass = LawnGrass("Трава", 25.0, 100, "USA", "14 дней", "Green")

        category.add_product(smartphone)
        category.add_product(lawn_grass)

        assert len(category.products) == 2


class TestExistingFunctionality:
    """Тесты для проверки существующей функциональности"""

    def test_existing_category_creation(self):
        """Тест что создание категории работает как раньше"""
        # Перехватываем вывод чтобы не мешал тестам
        captured_output = StringIO()
        sys.stdout = captured_output

        products = [
            Product("Товар1", 100.0, 5, "Описание товара 1"),
            Product("Товар2", 200.0, 3, "Описание товара 2")
        ]
        category = Category("Техника", "Электронные устройства", products)

        sys.stdout = sys.__stdout__

        assert category.name == "Техника"
        assert category.description == "Электронные устройства"
        assert len(category.products) == 2

    def test_existing_category_str(self):
        """Тест что строковое представление работает как раньше"""
        products = [
            Product("Товар1", 100.0, 5, "Описание товара 1"),
            Product("Товар2", 200.0, 3, "Описание товара 2"),
            Product("Товар3", 300.0, 1, "Описание товара 3")
        ]
        category = Category("Техника", "Электронные устройства", products)

        category_str = str(category)

        assert "Категория: Техника" in category_str
        assert "Описание: Электронные устройства" in category_str
        # Теперь проверяем правильный формат строки продукта
        assert "Товар1, 100 руб. Остаток: 5 шт." in category_str
        assert "Товар2, 200 руб. Остаток: 3 шт." in category_str
        assert "Товар3, 300 руб. Остаток: 1 шт." in category_str

    def test_existing_products_list(self):
        """Тест что products_list работает как раньше"""
        products = [
            Product("Товар1", 100.0, 5, "Описание товара 1"),
            Product("Товар2", 200.0, 3, "Описание товара 2")
        ]
        category = Category("Категория", "Описание категории", products)

        # Проверяем различные способы доступа
        assert len(category.products) == 2
        assert len(category.get_products()) == 2
        assert category.products_count == 2
        assert len(category) == 2

    def test_existing_total_value(self):
        """Тест что total_value работает как раньше"""
        products = [
            Product("Товар1", 100.0, 2, "Описание товара 1"),  # 200
            Product("Товар2", 50.0, 4, "Описание товара 2"),  # 200
            Product("Товар3", 300.0, 1, "Описание товара 3")  # 300
        ]
        category = Category("Категория", "Описание категории", products)

        # Проверяем информацию о продуктах
        products_info = category.get_products_info()
        assert len(products_info) == 3
        # Теперь total_value должен быть доступен
        assert products_info[0]['total_value'] == 200.0
        assert products_info[1]['total_value'] == 200.0
        assert products_info[2]['total_value'] == 300.0


def test_all_functionality_together():
    """Комплексный тест всей функциональности"""
    # Перехватываем вывод
    captured_output = StringIO()
    sys.stdout = captured_output

    # Создаем категорию
    electronics = Category("Электроника", "Техника и устройства")

    # Создаем разные типы продуктов
    laptop = Product("Ноутбук", 80000.0, 3, "Игровой ноутбук")
    smartphone = Smartphone("iPhone", 50000.0, 5, "15 Pro", 256, "Black")

    # Добавляем продукты в категорию
    electronics.add_product(laptop)
    electronics.add_product(smartphone)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    # Проверяем логирование
    assert "Создан объект Product(" in output
    assert "Создан объект Smartphone(" in output

    # Проверяем функциональность
    assert electronics.name == "Электроника"
    assert len(electronics.products) == 2
    assert electronics.products_count == 2

    # Проверяем специфичные методы
    assert smartphone.get_tech_specs()['model'] == "15 Pro"
    assert smartphone.get_tech_specs()['storage'] == 256


class TestCategory:
    """Основные тесты категории"""

    def test_category_creation(self):
        """Тест создания категории с продуктами"""
        # Перехватываем вывод
        captured_output = StringIO()
        sys.stdout = captured_output

        products = [
            Product("Товар1", 100.0, 5, "Описание товара 1"),
            Product("Товар2", 200.0, 3, "Описание товара 2")
        ]
        category = Category("Электроника", "Технические устройства", products)

        sys.stdout = sys.__stdout__

        assert category.name == "Электроника"
        assert category.description == "Технические устройства"
        assert len(category.products) == 2
        assert Category.total_categories >= 1

    def test_category_str_representation(self):
        """Тест строкового представления категории"""
        products = [
            Product("Товар1", 100.0, 5, "Описание товара 1"),
            Product("Товар2", 200.0, 3, "Описание товара 2"),
            Product("Товар3", 300.0, 1, "Описание товара 3")
        ]
        category = Category("Техника", "Электронные устройства", products)

        category_str = str(category)

        # Проверяем основные части строкового представления
        assert "Категория: Техника" in category_str
        assert "Описание: Электронные устройства" in category_str
        # Проверяем правильный формат строк продуктов
        assert "Товар1, 100 руб. Остаток: 5 шт." in category_str
        assert "Товар2, 200 руб. Остаток: 3 шт." in category_str
        assert "Товар3, 300 руб. Остаток: 1 шт." in category_str

    def test_category_products_list(self):
        """Тест получения списка продуктов категории"""
        products = [
            Product("Товар1", 100.0, 5, "Описание товара 1"),
            Product("Товар2", 200.0, 3, "Описание товара 2")
        ]
        category = Category("Категория", "Описание категории", products)

        # Проверяем, что продукты доступны
        products_list = category.get_products()
        assert len(products_list) == 2
        assert products_list[0].name == "Товар1"
        assert products_list[1].name == "Товар2"

    def test_category_total_value(self):
        """Тест общей стоимости продуктов в категории"""
        products = [
            Product("Товар1", 100.0, 2, "Описание товара 1"),  # 200
            Product("Товар2", 50.0, 4, "Описание товара 2"),  # 200
            Product("Товар3", 300.0, 1, "Описание товара 3")  # 300
        ]
        category = Category("Категория", "Описание категории", products)

        # Проверяем информацию о продуктах
        products_info = category.get_products_info()
        total_values = [info['total_value'] for info in products_info]

        assert total_values == [200.0, 200.0, 300.0]

    def test_product_and_category_integration(self):
        """Тест интеграции продукта и категории"""
        # Перехватываем вывод
        captured_output = StringIO()
        sys.stdout = captured_output

        # Создаем продукты
        laptop = Product("Ноутбук", 80000.0, 3, "Игровой ноутбук")
        phone = Product("Смартфон", 50000.0, 5, "Флагманский смартфон")
        tablet = Product("Планшет", 30000.0, 2, "Графический планшет")

        # Создаем категорию
        electronics = Category("Электроника", "Технические устройства")

        # Добавляем продукты в категорию
        electronics.add_product(laptop)
        electronics.add_product(phone)
        electronics.add_product(tablet)

        sys.stdout = sys.__stdout__

        # Проверяем результат
        assert electronics.name == "Электроника"
        assert len(electronics.products) == 3
        assert electronics.products_count == 3

        # Проверяем отдельные продукты
        products = electronics.get_products()
        assert products[0].name == "Ноутбук"
        assert products[1].name == "Смартфон"
        assert products[2].name == "Планшет"
