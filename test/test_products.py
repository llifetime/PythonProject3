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


class TestZeroQuantityExceptions:
    """Тесты для новой функциональности исключений с нулевым количеством"""

    def test_product_creation_with_zero_quantity_raises_value_error(self):
        """Тест, что создание товара с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Тестовый товар", 100.0, 0)

    def test_smartphone_creation_with_zero_quantity_raises_value_error(self):
        """Тест, что создание смартфона с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Smartphone("Тестовый смартфон", 500.0, 0, "Model X", 128, "Black")

    def test_lawn_grass_creation_with_zero_quantity_raises_value_error(self):
        """Тест, что создание газонной травы с нулевым количеством вызывает ValueError"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            LawnGrass("Тестовая трава", 50.0, 0, "Россия", "10 дней", "Зеленая")

    def test_category_add_product_with_zero_quantity_raises_zero_quantity_error(self):
        """Тест, что добавление товара с нулевым количеством в категорию вызывает исключение"""

        # Создаем mock объект с нулевым количеством
        class MockProduct:
            def __init__(self):
                self.name = "Тестовый товар"
                self.price = 100.0
                self.quantity = 0

            def get_description(self):
                return "Тестовое описание"

        category = Category("Тестовая категория", "Описание")
        mock_product = MockProduct()

        with pytest.raises(Exception) as exc_info:  # Может быть ZeroQuantityError или другое исключение
            category.add_product(mock_product)

        # Проверяем, что исключение было вызвано
        assert "нулевым количеством" in str(exc_info.value).lower() or "нельзя добавить" in str(exc_info.value).lower()

    def test_valid_product_creation_works_correctly(self):
        """Тест, что создание товара с положительным количеством работает корректно"""
        product = Product("Валидный товар", 100.0, 5, "Описание")

        assert product.name == "Валидный товар"
        assert product.price == 100.0
        assert product.quantity == 5
        assert product.description == "Описание"

    def test_category_add_valid_product_works_correctly(self):
        """Тест, что добавление валидного товара в категорию работает корректно"""
        # Перехватываем вывод чтобы не мешал тестам
        captured_output = StringIO()
        sys.stdout = captured_output

        category = Category("Тестовая категория", "Описание")
        product = Product("Валидный товар", 100.0, 5)

        # Это не вызовет исключение
        category.add_product(product)

        sys.stdout = sys.__stdout__

        assert len(category) == 1
        assert product in category.get_products()


class TestCategoryAveragePrice:
    """Тесты для новой функциональности расчета средней цены в категории"""

    def test_category_average_price_with_products(self):
        """Тест расчета средней цены в категории с товарами"""
        product1 = Product("Товар1", 100.0, 2)
        product2 = Product("Товар2", 300.0, 3)
        category = Category("Тестовая категория", "Описание", [product1, product2])

        expected_average = (100.0 + 300.0) / 2
        assert category.calculate_average_price() == expected_average

    def test_category_average_price_empty(self):
        """Тест расчета средней цены в пустой категории"""
        category = Category("Пустая категория", "Описание")

        assert category.calculate_average_price() == 0

    def test_category_average_price_single_product(self):
        """Тест расчета средней цены с одним товаром"""
        product = Product("Один товар", 150.0, 5)
        category = Category("Категория с одним товаром", "Описание", [product])

        assert category.calculate_average_price() == 150.0

    def test_category_average_price_after_adding_products(self):
        """Тест расчета средней цены после добавления товаров"""
        category = Category("Динамическая категория", "Описание")

        # Изначально средняя цена должна быть 0
        assert category.calculate_average_price() == 0

        # Добавляем товары
        product1 = Product("Товар1", 100.0, 2)
        product2 = Product("Товар2", 200.0, 3)

        # Перехватываем вывод при добавлении
        captured_output = StringIO()
        sys.stdout = captured_output

        category.add_product(product1)
        category.add_product(product2)

        sys.stdout = sys.__stdout__

        # Проверяем среднюю цену после добавления
        expected_average = (100.0 + 200.0) / 2
        assert category.calculate_average_price() == expected_average


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

        # Теперь нельзя создать продукт с нулевым количеством через конструктор
        # Но можно проверить поведение при уменьшении количества до 0
        product_available.quantity = 0
        assert not product_available.is_available()


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_product_with_zero_price(self):
        """Тест продукта с нулевой ценой"""
        product = Product("Free Product", 0.0, 10)
        assert product.calculate_total_value() == 0.0

    def test_product_with_negative_quantity(self):
        """Тест продукта с отрицательным количеством"""
        # Создаем продукт с положительным количеством, затем меняем на отрицательное
        product = Product("Test", 100.0, 5)
        product.quantity = -5
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

    def test_category_average_price_with_zero_price_products(self):
        """Тест средней цены с товарами с нулевой ценой"""
        product1 = Product("Бесплатный товар", 0.0, 5)
        product2 = Product("Платный товар", 200.0, 3)
        category = Category("Смешанная категория", "Описание", [product1, product2])

        expected_average = (0.0 + 200.0) / 2
        assert category.calculate_average_price() == expected_average


class TestIntegrationScenarios:
    """Интеграционные тесты для полных сценариев"""

    def test_complete_workflow_with_exceptions(self):
        """Тест полного рабочего процесса с обработкой исключений"""
        # Перехватываем вывод
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Пытаемся создать товар с нулевым количеством - должно вызвать исключение
            with pytest.raises(ValueError):
                Product("Недоступный товар", 100.0, 0)
        except ValueError:
            pass  # Ожидаемое исключение

        # Создаем валидные товары
        valid_product1 = Product("Валидный товар 1", 100.0, 10)
        valid_product2 = Product("Валидный товар 2", 200.0, 5)

        # Создаем категорию и добавляем товары
        category = Category("Основная категория", "Для тестирования")
        category.add_product(valid_product1)
        category.add_product(valid_product2)

        # Проверяем функциональность категории
        assert len(category) == 2
        assert category.calculate_average_price() == 150.0

        sys.stdout = sys.__stdout__

    def test_backward_compatibility(self):
        """Тест обратной совместимости со старым кодом"""
        # Все старые тесты должны продолжать работать

        # Создание продуктов с положительным количеством
        product1 = Product("Product1", 50.0, 10)
        product2 = Product("Product2", 150.0, 5)

        # Работа с категориями
        category = Category("Category", "Description", [product1, product2])

        # Проверка старой функциональности
        assert category.name == "Category"
        assert len(category.products) == 2
        assert product1 in category.products
        assert product2 in category.products

        # Проверка строковых представлений
        assert "Product1" in str(product1)
        assert "50" in str(product1)