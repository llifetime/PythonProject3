import pytest
from io import StringIO
import sys
from src.product import Product, Smartphone, LawnGrass, BaseProduct
from src.category import Category


class TestLoggingMixin:
    """Тесты для миксина логирования"""

    def capture_output(self):
        """Вспомогательный метод для перехвата вывода"""
        captured_output = StringIO()
        sys.stdout = captured_output
        return captured_output

    def restore_output(self):
        """Восстановление стандартного вывода"""
        sys.stdout = sys.__stdout__

    def test_product_creation_logging(self):
        """Тест логирования создания обычного продукта"""
        captured_output = self.capture_output()

        # Создаем продукт
        Product("Test Product", 100.0, 10, "Test Description")

        # Получаем вывод
        output = captured_output.getvalue().strip()
        self.restore_output()

        # Проверяем логирование
        assert "Создан объект Product(" in output
        assert "'Test Product'" in output
        assert "100.0" in output
        assert "10" in output

    def test_smartphone_creation_logging(self):
        """Тест логирования создания смартфона"""
        captured_output = self.capture_output()

        Smartphone("Test Phone", 500.0, 5, "Model X", 128, "Black")

        output = captured_output.getvalue().strip()
        self.restore_output()

        assert "Создан объект Smartphone(" in output
        assert "'Test Phone'" in output
        assert "500.0" in output
        assert "5" in output

    def test_lawn_grass_creation_logging(self):
        """Тест логирования создания газонной травы"""
        captured_output = self.capture_output()

        LawnGrass("Premium Grass", 25.0, 100, "USA", "14 дней", "Green")

        output = captured_output.getvalue().strip()
        self.restore_output()

        assert "Создан объект LawnGrass(" in output
        assert "'Premium Grass'" in output
        assert "25.0" in output
        assert "100" in output

    def test_logging_with_different_arguments(self):
        """Тест логирования с различными типами аргументов"""
        captured_output = self.capture_output()

        # Продукт без описания
        Product("Simple Product", 50.0, 20)

        output = captured_output.getvalue().strip()
        self.restore_output()

        assert "Создан объект Product(" in output
        assert "'Simple Product'" in output
        assert "50.0" in output
        assert "20" in output


class TestBaseProduct:
    """Тесты для базового абстрактного класса"""

    def test_base_product_is_abstract(self):
        """Тест, что BaseProduct является абстрактным"""
        with pytest.raises(TypeError):
            # Попытка создать экземпляр абстрактного класса должна вызывать ошибку
            BaseProduct("Test", 100.0, 10)

    def test_product_inherits_from_base_product(self):
        """Тест, что Product наследует от BaseProduct"""
        product = Product("Test", 100.0, 10)
        assert isinstance(product, BaseProduct)

    def test_abstract_methods_implementation(self):
        """Тест реализации абстрактных методов"""
        product = Product("Test", 100.0, 10, "Description")

        # Проверяем, что методы реализованы и работают
        assert product.get_description() == "Description"
        assert product.calculate_total_value() == 1000.0

    def test_base_product_functionality(self):
        """Тест функциональности унаследованной от BaseProduct"""
        product = Product("Test Product", 100.0, 5)

        # Проверяем основные атрибуты
        assert product.name == "Test Product"
        assert product.price == 100.0
        assert product.quantity == 5
        assert hasattr(product, 'created_at')

        # Проверяем методы BaseProduct
        assert product.is_available()

        product.apply_discount(10)
        assert product.price == 90.0

        product.increase_quantity(5)
        assert product.quantity == 10

        assert product.decrease_quantity(3)
        assert product.quantity == 7

        assert not product.decrease_quantity(10)  # Недостаточно товара
        assert product.quantity == 7

    def test_product_info_method(self):
        """Тест метода get_product_info"""
        product = Product("Test", 100.0, 5, "Test Description")
        info = product.get_product_info()

        assert info['name'] == "Test"
        assert info['price'] == 100.0
        assert info['quantity'] == 5
        assert info['total_value'] == 500.0
        assert info['is_available']
        assert 'created_at' in info


class TestInheritanceChain:
    """Тесты цепочки наследования"""

    def test_inheritance_hierarchy(self):
        """Тест иерархии наследования"""
        smartphone = Smartphone("Phone", 500.0, 10, "Model", 128, "Black")

        # Проверяем цепочку наследования
        assert isinstance(smartphone, Smartphone)
        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, BaseProduct)

    def test_method_resolution_order(self):
        """Тест порядка разрешения методов (MRO)"""
        mro = Smartphone.__mro__

        # Проверяем правильный порядок наследования
        assert mro[0] == Smartphone
        assert mro[1] == Product
        # LoggingMixin должен быть в цепочке
        assert any(cls.__name__ == 'LoggingMixin' for cls in mro)
        assert BaseProduct in mro


class TestExistingFunctionality:
    """Тесты для проверки существующей функциональности"""

    def capture_output(self):
        """Вспомогательный метод для перехвата вывода"""
        captured_output = StringIO()
        sys.stdout = captured_output
        return captured_output

    def restore_output(self):
        """Восстановление стандартного вывода"""
        sys.stdout = sys.__stdout__

    def test_category_with_products(self):
        """Тест работы категорий с продуктами (существующая функциональность)"""
        # Перехватываем вывод чтобы не мешал тестам
        self.capture_output()

        product1 = Product("Product 1", 100.0, 5)
        product2 = Product("Product 2", 200.0, 3)

        category = Category("Test Category", "Test Description", [product1, product2])

        self.restore_output()

        # Проверяем существующую функциональность
        assert category.name == "Test Category"
        assert len(category.products) == 2
        assert category.products_count == 2
        assert Category.total_categories >= 1

    def test_product_string_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Test Product", 150.0, 8)
        product_str = str(product)

        assert "Test Product" in product_str
        assert "150" in product_str
        assert "8" in product_str

    def test_smartphone_specific_functionality(self):
        """Тест специфичной функциональности смартфона"""
        smartphone = Smartphone("Phone", 500.0, 10, "Model X", 256, "Blue")

        specs = smartphone.get_tech_specs()
        assert specs['model'] == "Model X"
        assert specs['storage'] == 256
        assert specs['color'] == "Blue"

    def test_lawn_grass_specific_functionality(self):
        """Тест специфичной функциональности газонной травы"""
        lawn_grass = LawnGrass("Grass", 25.0, 100, "Germany", "10 дней", "Green")

        growing_info = lawn_grass.get_growing_info()
        assert growing_info['country'] == "Germany"
        assert growing_info['germination_period'] == "10 дней"
        assert growing_info['color'] == "Green"

    def test_category_products_access(self):
        """Тест доступа к продуктам в категории"""
        product = Product("Test", 100.0, 5)
        category = Category("Test Category", "Description", [product])

        # Проверяем различные способы доступа к продуктам
        assert len(category.products) == 1
        assert len(category.get_products()) == 1
        assert category.products_count == 1
        assert len(category) == 1

    def test_product_availability(self):
        """Тест проверки доступности продукта"""
        product_available = Product("Available", 100.0, 5)
        product_unavailable = Product("Unavailable", 100.0, 0)

        assert product_available.is_available()
        assert not product_unavailable.is_available()


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_product_with_zero_price(self):
        """Тест продукта с нулевой ценой"""
        product = Product("Free Product", 0.0, 10)
        assert product.calculate_total_value() == 0.0

    def test_product_with_negative_quantity(self):
        """Тест продукта с отрицательным количеством"""
        product = Product("Test", 100.0, -5)
        assert not product.is_available()

    def test_discount_edge_cases(self):
        """Тест граничных случаев скидок"""
        product = Product("Test", 100.0, 10)

        # Скидка 0%
        product.apply_discount(0)
        assert product.price == 100.0

        # Скидка 100%
        product.apply_discount(100)
        assert product.price == 0.0

        # Скидка больше 100% (должна игнорироваться)
        product.price = 100.0
        product.apply_discount(150)
        assert product.price == 100.0

        # Отрицательная скидка (должна игнорироваться)
        product.price = 100.0
        product.apply_discount(-10)
        assert product.price == 100.0
