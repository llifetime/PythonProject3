from src.category import Category
from src.product import Product


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

        # Проверяем products_list - ИСПРАВЛЕНО: ищем "Смартфон" вместо "Телефон"
        products_str = electronics.products_list
        assert "Ноутбук, 80000 руб. Остаток: 3 шт." in products_str
        assert "Смартфон, 50000 руб. Остаток: 5 шт." in products_str  # ← ИСПРАВЛЕНО ЗДЕСЬ
        assert "Планшет, 30000 руб. Остаток: 2 шт." in products_str
