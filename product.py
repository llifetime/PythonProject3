"""Module for Product and Category classes."""


class Product:
    """Represents a product in the store."""

    def __init__(self, name, description, price, quantity):
        """
        Initialize product instance.

        Args:
            name (str): Product name
            description (str): Product description
            price (float): Product price
            quantity (int): Quantity in stock
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        """Return string representation of product."""
        return f"{self.name} - {self.price} руб. (в наличии: {self.quantity})"


class Category:
    """Represents a product category."""

    # Class attributes
    total_categories = 0
    total_unique_products = 0

    def __init__(self, name, description, products=None):
        """
        Initialize category instance.

        Args:
            name (str): Category name
            description (str): Category description
            products (list, optional): List of products. Defaults to None.
        """
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Update class counters
        Category.total_categories += 1
        Category.total_unique_products += len(self.products)

    def add_product(self, product):
        """Add product to category."""
        self.products.append(product)
        Category.total_unique_products += 1

    def remove_product(self, product_name):
        """Remove product from category by name."""
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                Category.total_unique_products -= 1
                break

    def get_total_products(self):
        """Return total number of products in category."""
        return len(self.products)

    def get_total_quantity(self):
        """Return total quantity of all products in stock."""
        return sum(product.quantity for product in self.products)

    def __str__(self):
        """Return string representation of category."""
        return f"Категория: {self.name} ({self.get_total_products()} товаров)"
