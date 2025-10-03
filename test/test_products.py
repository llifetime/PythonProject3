import pytest

from src.product import Product
from src.category import sum_products


class TestProduct:

    """Тесты для класса Product"""

    def test_product_creation(self):
        """Тест создания продукта"""
        product = Product("Телефон", "Смартфон", 50000, 10)  # добавлено описание
        assert product.name == "Телефон"
        assert product.price == 50000
        assert product.quantity == 10

    def test_product_str_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Ноутбук", "Игровой ноутбук", 80000, 5)  # добавлено описание
        expected_str = "Ноутбук, 80000 руб. Остаток: 5 шт."
        assert str(product) == expected_str

    def test_product_str_with_different_values(self):
        """Тест строкового представления с разными значениями"""
        product = Product("Книга", "Художественная литература", 500, 0)  # добавлено описание
        expected_str = "Книга, 500 руб. Остаток: 0 шт."
        assert str(product) == expected_str

    def test_product_addition(self):
        product1 = Product("Товар1", "Описание1", 100, 10)  # 1000
        product2 = Product("Товар2", "Описание2", 200, 5)  # 1000
        result = product1 + product2
        assert result == 2000  # 1000 + 1000

    def test_product_addition_commutative(self):
        product1 = Product("A", "Описание A", 50, 4)  # 200
        product2 = Product("B", "Описание B", 30, 10)  # 300
        result1 = product1 + product2
        result2 = product2 + product1
        assert result1 == result2 == 500  # 200 + 300

    def test_product_addition_with_zero_quantity(self):
        """Тест сложения продуктов с нулевым количеством"""
        product1 = Product("Товар1", "Описание1", 100, 0)  # 0
        product2 = Product("Товар2", "Описание2", 200, 0)  # 0
        result = product1 + product2
        assert result == 0  # исправлено на правильное значение


    def test_product_addition_type_error(self):
        """Тест ошибки при сложении с неправильным типом"""
        product = Product("Товар", "Описание", 100, 5)  # добавлено описание

        # Тестируем с типом, который НЕ Product и НЕ число
        with pytest.raises(TypeError, match="Можно складывать только с Product или числами"):
            product + "неправильный тип"  # строка

    def test_product_addition_chain(self):
        """Тест цепочки сложений"""
        product1 = Product("A", "Описание A", 10, 3)  # 30
        product2 = Product("B", "Описание B", 20, 2)  # 40
        product3 = Product("C", "Описание C", 5, 10)  # 50
        result = (product1 + product2) + product3
        assert result == 120  # исправлено на правильное значение



class TestSumProductsFunction:
    """Тесты для вспомогательной функции sum_products"""

    def test_sum_products_basic(self):
        """Тест базового использования sum_products"""
        product1 = Product("A", "Описание A", 100, 2)  # 200
        product2 = Product("B", "Описание B", 50, 6)  # 300
        product3 = Product("C", "Описание C", 200, 1)  # 200
        total = sum_products(product1, product2, product3)
        assert total == 700

    def test_sum_products_single(self):
        """Тест sum_products с одним продуктом"""
        product = Product("Товар", "Описание", 150, 4)  # 600
        total = sum_products(product)
        assert total == 600

    def test_sum_products_empty(self):
        """Тест sum_products без аргументов"""
        total = sum_products()
        assert total == 0

    def test_sum_products_type_error(self):
        """Тест ошибок в sum_products"""
        product = Product("Товар", "Описание", 100, 1)  # добавлено описание

        with pytest.raises(TypeError, match="Все аргументы должны быть объектами Product"):
            sum_products(product, "invalid")

        with pytest.raises(TypeError, match="Все аргументы должны быть объектами Product"):
            sum_products(123, product)
