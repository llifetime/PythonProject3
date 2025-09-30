import pytest

from product import Product, Category, sum_products


class TestProduct:
    """Тесты для класса Product"""
    
    def test_product_creation(self):
        """Тест создания продукта"""
        product = Product("Телефон", 50000, 10)
        assert product.name == "Телефон"
        assert product.price == 50000
        assert product.quantity == 10
    
    def test_product_str_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Ноутбук", 80000, 5)
        expected_str = "Ноутбук, 80000 руб. Остаток: 5 шт."
        assert str(product) == expected_str
    
    def test_product_str_with_different_values(self):
        """Тест строкового представления с разными значениями"""
        product = Product("Книга", 500, 0)
        expected_str = "Книга, 500 руб. Остаток: 0 шт."
        assert str(product) == expected_str
    
    def test_product_addition(self):
        """Тест сложения двух продуктов"""
        product1 = Product("Товар1", 100, 10)  # 100 * 10 = 1000
        product2 = Product("Товар2", 200, 2)   # 200 * 2 = 400
        
        result = product1 + product2
        assert result == 1400  # 1000 + 400
    
    def test_product_addition_commutative(self):
        """Тест коммутативности сложения"""
        product1 = Product("A", 50, 4)  # 200
        product2 = Product("B", 30, 6)  # 180
        
        result1 = product1 + product2
        result2 = product2 + product1
        assert result1 == result2 == 380
    
    def test_product_addition_with_zero_quantity(self):
        """Тест сложения продуктов с нулевым количеством"""
        product1 = Product("Товар1", 100, 0)  # 0
        product2 = Product("Товар2", 200, 5)  # 1000
        
        result = product1 + product2
        assert result == 1000
    
    def test_product_addition_type_error(self):
        """Тест ошибки при сложении с неправильным типом"""
        product = Product("Товар", 100, 5)
        
        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + 100
        
        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + "string"
    
    def test_product_addition_chain(self):
        """Тест цепочки сложений"""
        product1 = Product("A", 10, 3)  # 30
        product2 = Product("B", 20, 2)  # 40
        product3 = Product("C", 30, 1)  # 30
        
        result = (product1 + product2) + product3
        assert result == 100


class TestCategory:
    """Тесты для класса Category"""
    
    def test_category_creation(self):
        """Тест создания категории"""
        products = [
            Product("Товар1", 100, 5),
            Product("Товар2", 200, 3)
        ]
        category = Category("Электроника")
        
        assert category.name == "Электроника"
        assert len(category.products) == 2
    
    def test_category_str_representation(self):
        """Тест строкового представления категории"""
        products = [
            Product("Товар1", 100, 5),
            Product("Товар2", 200, 3),
            Product("Товар3", 300, 1)
        ]
        category = Category("Техника")
        
        expected_str = "Техника, количество продуктов: 3 шт."
        assert str(category) == expected_str
    
    def test_category_str_empty(self):
        """Тест строкового представления пустой категории"""
        category = Category("Пустая категория")
        
        expected_str = "Пустая категория, количество продуктов: 0 шт."
        assert str(category) == expected_str
    
    def test_category_products_list(self):
        """Тест геттера products_list"""
        products = [
            Product("Товар1", 100, 5),
            Product("Товар2", 200, 3)
        ]
        category = Category("Категория")
        
        products_list = category.products_list
        expected_output = "Товар1, 100 руб. Остаток: 5 шт.\nТовар2, 200 руб. Остаток: 3 шт."
        assert products_list == expected_output
    
    def test_category_products_list_empty(self):
        """Тест геттера products_list для пустой категории"""
        category = Category("Пустая")
        
        products_list = category.products_list
        assert products_list == ""
    
    def test_category_total_value(self):
        """Тест расчета общей стоимости товаров в категории"""
        products = [
            Product("Товар1", 100, 2),  # 200
            Product("Товар2", 50, 4),   # 200
            Product("Товар3", 300, 1)   # 300
        ]
        category = Category("Категория")
        
        total_value = category.total_value()
        assert total_value == 700  # 200 + 200 + 300
    
    def test_category_total_value_empty(self):
        """Тест расчета общей стоимости для пустой категории"""
        category = Category("Пустая")
        
        total_value = category.total_value()
        assert total_value == 0


class TestIntegration:
    """Интеграционные тесты"""

    def test_product_and_category_integration(self):
        """Интеграционный тест продукта и категории"""
        # Создаем продукты
        laptop = Product("Ноутбук", 80000, 3)
        phone = Product("Телефон", 50000, 5)
        tablet = Product("Планшет", 30000, 2)

        # Создаем категорию
        electronics = Category("Электроника")

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

        # Проверяем products_list
        products_str = electronics.products_list
        assert "Ноутбук, 80000 руб. Остаток: 3 шт." in products_str
        assert "Телефон, 50000 руб. Остаток: 5 шт." in products_str
        assert "Планшет, 30000 руб. Остаток: 2 шт." in products_str

        # Проверяем вспомогательную функцию
        total_sum = sum_products(laptop, phone, tablet)
        assert total_sum == expected_total


def test_backward_compatibility():
    """Тест обратной совместимости со старым кодом"""
    # Старый код должен продолжать работать
    product = Product("Товар", 100, 5)
    assert hasattr(product, 'name')
    assert hasattr(product, 'price')
    assert hasattr(product, 'quantity')

    # Старые методы должны работать
    category = Category("Категория")
    assert hasattr(category, 'name')
    assert hasattr(category, 'products')
    assert hasattr(category, 'products_list')


class TestSumProductsFunction:
    """Тесты для вспомогательной функции sum_products"""

    def test_sum_products_basic(self):
        """Тест базового использования sum_products"""
        product1 = Product("A", 100, 2)  # 200
        product2 = Product("B", 50, 6)  # 300
        product3 = Product("C", 200, 1)  # 200

        total = sum_products(product1, product2, product3)
        assert total == 700

    def test_sum_products_single(self):
        """Тест sum_products с одним продуктом"""
        product = Product("Товар", 150, 4)  # 600
        total = sum_products(product)
        assert total == 600

    def test_sum_products_empty(self):
        """Тест sum_products без аргументов"""
        total = sum_products()
        assert total == 0

    def test_sum_products_type_error(self):
        """Тест ошибок в sum_products"""
        product = Product("Товар", 100, 1)

        with pytest.raises(TypeError, match="Все аргументы должны быть объектами Product"):
            sum_products(product, "invalid")

        with pytest.raises(TypeError, match="Все аргументы должны быть объектами Product"):
            sum_products(123, product)