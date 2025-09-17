"""Pytest tests for Product and Category classes."""

import pytest
from product import Product, Category


class TestProductPytest:
    """Test cases for Product class using pytest."""

    def test_product_initialization(self):
        """Test that Product initializes correctly with all attributes."""
        product = Product("Test Product", "Test Description", 100.0, 10)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0
        assert product.quantity == 10

    def test_product_string_representation(self):
        """Test the string representation of Product."""
        product = Product("Test Product", "Test Description", 100.0, 10)
        expected_string = "Test Product - 100.0 руб. (в наличии: 10)"

        assert str(product) == expected_string

    def test_product_with_different_data_types(self):
        """Test Product with different data types."""
        product = Product("Name", "Desc", 99.99, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    @pytest.mark.parametrize("name,description,price,quantity", [
        ("Product A", "Desc A", 100.0, 5),
        ("Product B", "Desc B", 200.0, 10),
        ("Product C", "Desc C", 300.0, 15),
    ])
    def test_product_parametrized(self, name, description, price, quantity):
        """Test Product with parametrized data."""
        product = Product(name, description, price, quantity)

        assert product.name == name
        assert product.description == description
        assert product.price == price
        assert product.quantity == quantity


class TestCategoryPytest:
    """Test cases for Category class using pytest."""

    @pytest.fixture(autouse=True)
    def reset_counters(self):
        """Reset class counters before each test."""
        Category.total_categories = 0
        Category.total_unique_products = 0
        yield
        # Cleanup after test if needed

    @pytest.fixture
    def sample_products(self):
        """Fixture providing sample products."""
        return [
            Product("Product 1", "Description 1", 100.0, 5),
            Product("Product 2", "Description 2", 200.0, 10)
        ]

    def test_category_initialization_empty(self):
        """Test Category initialization without products."""
        category = Category("Test Category", "Test Description")

        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category.products) == 0
        assert category.get_total_products() == 0
        assert category.get_total_quantity() == 0

    def test_category_initialization_with_products(self, sample_products):
        """Test Category initialization with products list."""
        category = Category("Test Category", "Test Description", sample_products)

        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category.products) == 2
        assert category.get_total_products() == 2
        assert category.get_total_quantity() == 15  # 5 + 10

    def test_category_string_representation(self):
        """Test the string representation of Category."""
        category = Category("Test Category", "Test Description")
        assert str(category) == "Категория: Test Category (0 товаров)"

    def test_add_product_to_category(self, sample_products):
        """Test adding a product to category."""
        category = Category("Test Category", "Test Description")

        assert len(category.products) == 0
        assert category.get_total_products() == 0

        category.add_product(sample_products[0])
        assert len(category.products) == 1
        assert category.get_total_products() == 1
        assert category.products[0].name == "Product 1"

    def test_remove_product_from_category(self, sample_products):
        """Test removing a product from category."""
        category = Category("Test Category", "Test Description", sample_products)

        assert len(category.products) == 2

        category.remove_product("Product 1")
        assert len(category.products) == 1
        assert category.products[0].name == "Product 2"

        # Try to remove non-existent product
        category.remove_product("Non-existent")
        assert len(category.products) == 1  # Should remain unchanged


class TestCategoryCountersPytest:
    """Test cases for Category class counters using pytest."""

    @pytest.fixture(autouse=True)
    def reset_counters(self):
        """Reset class counters before each test."""
        Category.total_categories = 0
        Category.total_unique_products = 0
        yield

    def test_category_count_empty(self):
        """Test category counter with empty categories."""
        assert Category.total_categories == 0
        assert Category.total_unique_products == 0

    def test_category_count_single_empty(self):
        """Test counters with single empty category."""
        category = Category("Test Category", "Test Description")

        assert Category.total_categories == 1
        assert Category.total_unique_products == 0
        assert category.get_total_products() == 0

    def test_category_count_with_products(self):
        """Test counters with category containing products."""
        product1 = Product("P1", "D1", 100, 5)
        product2 = Product("P2", "D2", 200, 10)

        category = Category("Test Category", "Test Description", [product1, product2])

        assert Category.total_categories == 1
        assert Category.total_unique_products == 2
        assert category.get_total_products() == 2

    @pytest.mark.parametrize("product_count,expected_total", [
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
    ])
    def test_category_count_parametrized(self, product_count, expected_total):
        """Test category counters with parametrized product counts."""
        products = [
            Product(f"Product {i}", f"Description {i}", 100 * i, i * 5)
            for i in range(product_count)
        ]

        category = Category("Test Category", "Test Description", products)

        assert Category.total_categories == 1
        assert Category.total_unique_products == expected_total
        assert category.get_total_products() == expected_total


class TestIntegrationPytest:
    """Integration tests for Product and Category interaction using pytest."""

    @pytest.fixture(autouse=True)
    def reset_counters(self):
        """Reset class counters before each test."""
        Category.total_categories = 0
        Category.total_unique_products = 0
        yield

    @pytest.fixture
    def sample_products(self):
        """Fixture providing sample products."""
        return [
            Product("Phone", "Smartphone", 50000, 3),
            Product("Tablet", "Tablet PC", 30000, 2),
            Product("Laptop", "Notebook", 80000, 1)
        ]

    def test_multiple_operations(self, sample_products):
        """Test complex scenario with multiple operations."""
        # Create category with products
        electronics = Category("Electronics", "Electronic devices", sample_products[:2])
        assert Category.total_categories == 1
        assert Category.total_unique_products == 2
        assert electronics.get_total_quantity() == 5  # 3 + 2

        # Create another category
        computers = Category("Computers", "Computer equipment", [sample_products[2]])
        assert Category.total_categories == 2
        assert Category.total_unique_products == 3
        assert computers.get_total_quantity() == 1

        # Add product to existing category
        new_product = Product("Mouse", "Computer mouse", 2000, 10)
        computers.add_product(new_product)
        assert Category.total_unique_products == 4
        assert computers.get_total_quantity() == 11  # 1 + 10

        # Remove product
        computers.remove_product("Laptop")
        assert Category.total_unique_products == 3
        assert computers.get_total_quantity() == 10

    def test_edge_case_empty_category_operations(self):
        """Test edge cases with empty categories."""
        category = Category("Empty", "Empty category")

        assert category.get_total_products() == 0
        assert category.get_total_quantity() == 0

        # Try to remove from empty category
        category.remove_product("Non-existent")
        assert category.get_total_products() == 0
