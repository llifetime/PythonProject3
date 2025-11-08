import pytest
from src.product import Product, Smartphone, LawnGrass
from src.category import Category


class TestCategoryProductProtection:
    """Тесты защиты метода add_product"""

    def test_add_product_valid_types(self):
        """Тест добавления допустимых типов продуктов"""
        category = Category("Тестовая категория")

        # Создаем продукты разных допустимых типов
        product = Product("Товар", "Описание товара", 100, 5)
        smartphone = Smartphone(
            "iPhone", "Смартфон", 100000, 2,
            "Высокая", "15 Pro", 256, "Black"
        )
        lawn_grass = LawnGrass(
            "Трава", "Газонная трава", 5000, 10,
            "Россия", 14, "Зеленый"
        )

        # Все эти добавления должны работать без ошибок
        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(lawn_grass)

        # Проверяем, что продукты добавлены
        assert len(category) == 3
        assert product in category.products
        assert smartphone in category.products
        assert lawn_grass in category.products

    def test_add_product_invalid_string(self):
        """Тест попытки добавления строки"""
        category = Category("Тестовая категория")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product("не продукт")

        # Убеждаемся, что категория осталась пустой
        assert len(category) == 0

    def test_add_product_invalid_number(self):
        """Тест попытки добавления числа"""
        category = Category("Тестовая категория")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(123)

        assert len(category) == 0

    def test_add_product_invalid_list(self):
        """Тест попытки добавления списка"""
        category = Category("Тестовая категория")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(["item1", "item2"])

        assert len(category) == 0

    def test_add_product_invalid_dict(self):
        """Тест попытки добавления словаря"""
        category = Category("Тестовая категория")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product({"name": "product"})

        assert len(category) == 0

    def test_add_product_invalid_none(self):
        """Тест попытки добавления None"""
        category = Category("Тестовая категория")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(None)

        assert len(category) == 0

    def test_add_product_mixed_valid_invalid(self):
        """Тест смешанного добавления допустимых и недопустимых объектов"""
        category = Category("Тестовая категория")

        valid_product = Product("Товар", "Описание", 100, 5)

        # Добавляем допустимый продукт
        category.add_product(valid_product)
        assert len(category) == 1

        # Пытаемся добавить недопустимый объект
        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product("не продукт")

        # Убеждаемся, что предыдущий продукт остался, а новый не добавился
        assert len(category) == 1
        assert valid_product in category.products

    def test_add_product_inheritance_works(self):
        """Тест что наследование работает корректно"""
        category = Category("Тестовая категория")

        # Создаем наследников Product
        smartphone = Smartphone(
            "Phone", "Description", 50000, 3,
            "Medium", "Model X", 128, "Blue"
        )
        lawn_grass = LawnGrass(
            "Grass", "Description", 2000, 20,
            "Germany", 10, "Dark Green"
        )

        # Наследники должны добавляться без ошибок
        category.add_product(smartphone)
        category.add_product(lawn_grass)

        assert len(category) == 2
        assert smartphone in category.products
        assert lawn_grass in category.products


class TestExistingFunctionality:
    """Тесты для проверки что существующая функциональность не сломана"""

    def test_existing_category_creation(self):
        """Тест что создание категории работает как раньше"""
        products = [
            Product("Товар1", "Описание товара 1", 100, 5),
            Product("Товар2", "Описание товара 2", 200, 3)
        ]
        category = Category("Электроника", "Техника и гаджеты", products)

        assert category.name == "Электроника"
        assert category.description == "Техника и гаджеты"
        assert len(category) == 2

    def test_existing_category_str(self):
        """Тест что строковое представление работает как раньше"""
        products = [
            Product("Товар1", "Описание товара 1", 100, 5),
            Product("Товар2", "Описание товара 2", 200, 3),
            Product("Товар3", "Описание товара 3", 300, 1)
        ]
        category = Category("Техника")

        for product in products:
            category.add_product(product)

        expected_str = "Техника, количество продуктов: 3 шт."
        assert str(category) == expected_str

    def test_existing_products_list(self):
        """Тест что products_list работает как раньше"""
        products = [
            Product("Товар1", "Описание товара 1", 100, 5),
            Product("Товар2", "Описание товара 2", 200, 3)
        ]
        category = Category("Категория")

        for product in products:
            category.add_product(product)

        products_list = category.products_list
        expected_output = "Товар1, 100 руб. Остаток: 5 шт.\nТовар2, 200 руб. Остаток: 3 шт."
        assert products_list == expected_output

    def test_existing_total_value(self):
        """Тест что total_value работает как раньше"""
        products = [
            Product("Товар1", "Описание товара 1", 100, 2),  # 200
            Product("Товар2", "Описание товара 2", 50, 4),  # 200
            Product("Товар3", "Описание товара 3", 300, 1)  # 300
        ]
        category = Category("Категория")

        for product in products:
            category.add_product(product)

        total_value = category.total_value()
        assert total_value == 700  # 200 + 200 + 300


def test_all_functionality_together():
    """Комплексный тест всей функциональности"""
    # Создаем категорию
    electronics = Category("Электроника", "Техника и устройства")

    # Создаем разные типы продуктов
    laptop = Product("Ноутбук", "Игровой ноутбук", 80000, 3)
    smartphone = Smartphone(
        "iPhone", "Флагманский смартфон", 50000, 5,
        "Высокая", "15 Pro", 256, "Black"
    )

    # Добавляем продукты (должно работать)
    electronics.add_product(laptop)
    electronics.add_product(smartphone)

    # Проверяем базовую функциональность
    assert len(electronics) == 2
    assert str(electronics) == "Электроника, количество продуктов: 2 шт."

    # Проверяем products_list
    products_str = electronics.products_list

    # Для Product используется: "Ноутбук, 80000 руб. Остаток: 3 шт."
    assert "Ноутбук, 80000 руб. Остаток: 3 шт." in products_str

    # Для Smartphone используется: "Смартфон iPhone (15 Pro), Black, 256GB, 50000 руб."
    assert "Смартфон iPhone (15 Pro), Black, 256GB, 50000 руб." in products_str

    # Проверяем total_value
    total = electronics.total_value()
    expected_total = 80000 * 3 + 50000 * 5
    assert total == expected_total

    # Проверяем защиту от неверных типов
    with pytest.raises(TypeError):
        electronics.add_product("invalid product")

    # Убеждаемся, что после ошибки категория не изменилась
    assert len(electronics) == 2


class TestCategory:
    """Тесты для класса Category"""

    def test_category_creation(self):
        products = [
            Product("Товар1", "Описание товара 1", 100, 5),  # добавлено описание
            Product("Товар2", "Описание товара 2", 200, 3)  # добавлено описание
        ]
        category = Category("Электроника")

        # ДОБАВЛЯЕМ товары!
        for product in products:
            category.add_product(product)

        assert category.name == "Электроника"
        assert len(category.products) == 2  # Теперь будет 2

    def test_category_str_representation(self):
        products = [
            Product("Товар1", "Описание товара 1", 100, 5),
            Product("Товар2", "Описание товара 2", 200, 3),
            Product("Товар3", "Описание товара 3", 300, 1)
        ]
        category = Category("Техника")

        # ДОБАВЛЯЕМ товары!
        for product in products:
            category.add_product(product)

        expected_str = "Техника, количество продуктов: 3 шт."
        assert str(category) == expected_str  # Теперь будет 3

    def test_category_products_list(self):
        products = [
            Product("Товар1", "Описание товара 1", 100, 5),
            Product("Товар2", "Описание товара 2", 200, 3)
        ]
        category = Category("Категория")

        # ДОБАВЛЯЕМ товары!
        for product in products:
            category.add_product(product)

        products_list = category.products_list
        expected_output = "Товар1, 100 руб. Остаток: 5 шт.\nТовар2, 200 руб. Остаток: 3 шт."
        assert products_list == expected_output  # Теперь не пустая строка

    def test_category_total_value(self):
        products = [
            Product("Товар1", "Описание товара 1", 100, 2),  # 200
            Product("Товар2", "Описание товара 2", 50, 4),  # 200
            Product("Товар3", "Описание товара 3", 300, 1)  # 300
        ]
        category = Category("Категория")

        # ДОБАВЛЯЕМ товары!
        for product in products:
            category.add_product(product)

        total_value = category.total_value()
        assert total_value == 700  # 200 + 200 + 300 = 700 ✓

    def test_product_and_category_integration(self):
        # Создаем продукты
        laptop = Product("Ноутбук", "Игровой ноутбук", 80000, 3)
        phone = Product("Смартфон", "Флагманский смартфон", 50000, 5)
        tablet = Product("Планшет", "Графический планшет", 30000, 2)

        # Создаем категорию
        electronics = Category("Электроника")

        # Добавляем товары в категорию
        electronics.add_product(laptop)
        electronics.add_product(phone)
        electronics.add_product(tablet)

        # Проверяем строковые представления
        assert str(laptop) == "Ноутбук, 80000 руб. Остаток: 3 шт."
        assert str(electronics) == "Электроника, количество продуктов: 3 шт."

        # Проверяем сложение продуктов
        laptop_phone_total = laptop + phone
        assert laptop_phone_total == 80000 * 3 + 50000 * 5

        # Проверяем общую стоимость категории
        category_total = electronics.total_value()
        expected_total = 80000 * 3 + 50000 * 5 + 30000 * 2
        assert category_total == expected_total

        # Проверяем products_list - теперь это строка
        products_str = electronics.products_list
        assert "Ноутбук, 80000 руб. Остаток: 3 шт." in products_str
        assert "Смартфон, 50000 руб. Остаток: 5 шт." in products_str
        assert "Планшет, 30000 руб. Остаток: 2 шт." in products_str
