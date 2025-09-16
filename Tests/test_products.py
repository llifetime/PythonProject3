"""Tests for Product and Category classes."""

import unittest
from product import Product, Category


class TestProduct(unittest.TestCase):
    """Test cases for Product class."""

    def test_product_initialization(self):
        """Test that Product initializes correctly with all attributes."""
        product = Product("Test Product", "Test Description", 100.0, 10)

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Description")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.quantity, 10)

    def test_product_string_representation(self):
        """Test the string representation of Product."""
        product = Product("Test Product", "Test Description", 100.0, 10)
        expected_string = "Test Product - 100.0 руб. (в наличии: 10)"

        self.assertEqual(str(product), expected_string)

    def test_product_with_different_data_types(self):
        """Test Product with different data types."""
        product = Product("Name", "Desc", 99.99, 5)

        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.description, str)
        self.assertIsInstance(product.price, float)
        self.assertIsInstance(product.quantity, int)


class TestCategory(unittest.TestCase):
    """Test cases for Category class."""

    def setUp(self):
        """Reset class counters before each test."""
        Category.total_categories = 0
        Category.total_unique_products = 0
        self.product1 = Product("Product 1", "Description 1", 100.0, 5)
        self.product2 = Product("Product 2", "Description 2", 200.0, 10)

    def test_category_initialization_empty(self):
        """Test Category initialization without products."""
        category = Category("Test Category", "Test Description")

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Description")
        self.assertEqual(len(category.products), 0)
        self.assertEqual(category.get_total_products(), 0)
        self.assertEqual(category.get_total_quantity(), 0)

    def test_category_initialization_with_products(self):
        """Test Category initialization with products list."""
        products = [self.product1, self.product2]
        category = Category("Test Category", "Test Description", products)

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Description")
        self.assertEqual(len(category.products), 2)
        self.assertEqual(category.get_total_products(), 2)
        self.assertEqual(category.get_total_quantity(), 15)  # 5 + 10

    def test_category_string_representation(self):
        """Test the string representation of Category."""
        category = Category("Test Category", "Test Description")
        expected_string = "Категория: Test Category (0 товаров)"

        self.assertEqual(str(category), expected_string)

        # Test with products
        category_with_products = Category("Test", "Desc", [self.product1])
        expected_with_products = "Категория: Test (1 товаров)"
        self.assertEqual(str(category_with_products), expected_with_products)

    def test_add_product_to_category(self):
        """Test adding a product to category."""
        category = Category("Test Category", "Test Description")

        # Initially empty
        self.assertEqual(len(category.products), 0)
        self.assertEqual(category.get_total_products(), 0)

        # Add product
        category.add_product(self.product1)
        self.assertEqual(len(category.products), 1)
        self.assertEqual(category.get_total_products(), 1)
        self.assertEqual(category.products[0].name, "Product 1")

    def test_remove_product_from_category(self):
        """Test removing a product from category."""
        products = [self.product1, self.product2]
        category = Category("Test Category", "Test Description", products)

        self.assertEqual(len(category.products), 2)

        # Remove product
        category.remove_product("Product 1")
        self.assertEqual(len(category.products), 1)
        self.assertEqual(category.products[0].name, "Product 2")

        # Try to remove non-existent product
        category.remove_product("Non-existent")
        self.assertEqual(len(category.products), 1)  # Should remain unchanged


class TestCategoryCounters(unittest.TestCase):
    """Test cases for Category class counters."""

    def setUp(self):
        """Reset class counters before each test."""
        Category.total_categories = 0
        Category.total_unique_products = 0

    def test_category_count_empty(self):
        """Test category counter with empty categories."""
        self.assertEqual(Category.total_categories, 0)
        self.assertEqual(Category.total_unique_products, 0)

    def test_add_product_after_creation(self):
        """Test counters when adding products after category creation."""
        category = Category("Test Category", "Test Description")
        self.assertEqual(Category.total_unique_products, 0)

        product = Product("New Product", "Description", 100, 5)
        category.add_product(product)

        self.assertEqual(Category.total_unique_products, 1)
        self.assertEqual(category.get_total_products(), 1)

    def test_remove_product_affects_counters(self):
        """Test that removing products affects the counters."""
        product1 = Product("P1", "D1", 100, 5)
        product2 = Product("P2", "D2", 200, 10)

        category = Category("Test Category", "Test Description", [product1, product2])
        self.assertEqual(Category.total_unique_products, 2)

        category.remove_product("P1")
        self.assertEqual(Category.total_unique_products, 1)
        self.assertEqual(category.get_total_products(), 1)

    def test_get_total_quantity(self):
        """Test total quantity calculation."""
        product1 = Product("P1", "D1", 100, 5)
        product2 = Product("P2", "D2", 200, 10)
        product3 = Product("P3", "D3", 300, 15)

        category = Category("Test Category", "Test Description",
                            [product1, product2, product3])

        self.assertEqual(category.get_total_quantity(), 30)  # 5 + 10 + 15


class TestIntegration(unittest.TestCase):
    """Integration tests for Product and Category interaction."""

    def setUp(self):
        """Reset class counters before each test."""
        Category.total_categories = 0
        Category.total_unique_products = 0

    def test_multiple_operations(self):
        """Test complex scenario with multiple operations."""
        # Create products
        products = [
            Product("Phone", "Smartphone", 50000, 3),
            Product("Tablet", "Tablet PC", 30000, 2),
            Product("Laptop", "Notebook", 80000, 1)
        ]

        # Create category with products
        electronics = Category("Electronics", "Electronic devices", products[:2])
        self.assertEqual(Category.total_categories, 1)
        self.assertEqual(Category.total_unique_products, 2)
        self.assertEqual(electronics.get_total_quantity(), 5)  # 3 + 2

        # Create another category
        computers = Category("Computers", "Computer equipment", [products[2]])
        self.assertEqual(Category.total_categories, 2)
        self.assertEqual(Category.total_unique_products, 3)
        self.assertEqual(computers.get_total_quantity(), 1)

        # Add product to existing category
        new_product = Product("Mouse", "Computer mouse", 2000, 10)
        computers.add_product(new_product)
        self.assertEqual(Category.total_unique_products, 4)
        self.assertEqual(computers.get_total_quantity(), 11)  # 1 + 10

        # Remove product
        computers.remove_product("Laptop")
        self.assertEqual(Category.total_unique_products, 3)
        self.assertEqual(computers.get_total_quantity(), 10)


if __name__ == "__main__":
    unittest.main()
