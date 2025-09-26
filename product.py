"""Module for Product and Category classes."""
from typing import List, Optional


class Product:
    """Represents a product in the store."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Initialize product instance.

        Args:
            name (str): Product name
            description (str): Product description
            price (float): Product price
            quantity (int): Quantity in stock
        """
        self.name: str = name
        self.description: str = description
        self.price: float = price
        self.quantity: int = quantity

    @classmethod
    def new_product(cls, product_data):
        """Улучшенная версия с проверками"""
        try:
            # Проверяем, что все необходимые поля есть
            required_fields = ['name', 'price', 'quantity']
            for field in required_fields:
                if field not in product_data:
                    raise ValueError(f"Отсутствует поле: {field}")

            # Создаем товар
            return cls(
                name=product_data['name'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )

        except Exception as e:
            print(f"Ошибка создания товара: {e}")
            return None
            # Геттер для цены (позволяет читать цену)

        @property
        def price(self):
            """Возвращает текущую цену товара"""
            return self.__price

        # Сеттер для цены (позволяет изменять цену с проверкой)
        @price.setter
        def price(self, new_price):
            """Устанавливает новую цену с проверкой"""
            if new_price <= 0:
                print("Цена не должна быть нулевая или отрицательная")
                # НЕ устанавливаем новую цену, оставляем старую
            else:
                self.__price = new_price
                print(f"Цена товара '{self.name}' изменена на {new_price} руб.")

    def __str__(self) -> str:
        """Return string representation of product."""
        return f"{self.name} - {self.price} руб. (в наличии: {self.quantity})"


class Category:
    """Represents a product category."""

    # Class attributes
    total_categories: int = 0
    total_unique_products: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        """
        Initialize category instance.

        Args:
            name (str): Category name
            description (str): Category description
            products (list, optional): List of products. Defaults to None.
        """
        self.name: str = name
        self.description: str = description
        self.__products: List[Product] = products if products is not None else []

        # Update class counters
        Category.total_categories += 1
        Category.total_unique_products += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Add product to category."""
        self.__products.append(product)
        Category.total_unique_products += 1

    @property
    def products(self):
        """Геттер для просмотра товаров в нужном формате"""
        if not self.__products:
            return "В категории нет товаров"

        result = []
        for product in self.__products:
            # Форматируем по шаблону: "Название, цена руб. Остаток: кол-во шт."
            product_info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            result.append(product_info)

        return "\n".join(result)  # объединяем все строки через перенос

    def remove_product(self, product_name: str) -> None:
        """Remove product from category by name."""
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                Category.total_unique_products -= 1
                break

    def get_total_products(self) -> int:
        """Return total number of products in category."""
        return len(self.products)

    def get_total_quantity(self) -> int:
        """Return total quantity of all products in stock."""
        return sum(product.quantity for product in self.products)

    def __str__(self) -> str:
        """Return string representation of category."""
        return f"Категория: {self.name} ({self.get_total_products()} товаров)"
