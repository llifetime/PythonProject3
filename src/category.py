from src.product import Product


class Category:
    """Класс для категорий товаров"""

    # Атрибуты класса
    total_categories = 0
    product_count = 0

    def __init__(self, name, description="", products=None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        # Увеличиваем счетчики при создании категории
        Category.total_categories += 1
        Category.product_count += len(self.__products)

    @property
    def products(self):
        """Геттер для списка продуктов"""
        return self.__products

    def add_product(self, product):
        """Добавление продукта в категорию"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self):
        """Строковое представление категории - только название и количество"""
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."

    def __len__(self):
        """Количество продуктов в категории"""
        return len(self.__products)

    @classmethod
    def get_total_categories(cls):
        """Получить общее количество категорий"""
        return cls.total_categories

    @classmethod
    def get_product_count(cls):
        """Получить общее количество продуктов"""
        return cls.product_count

    @property
    def products_list(self):
        """Строковое представление списка продуктов"""
        return '\n'.join(str(product) for product in self.__products)

    def total_value(self):
        """Общая стоимость всех продуктов в категории"""
        return sum(product.price * product.quantity for product in self.__products)


def sum_products(*products):
    """Складывает стоимость нескольких продуктов"""
    total = 0
    for product in products:
        if not isinstance(product, Product):
            raise TypeError("Все аргументы должны быть объектами Product")
        total += product.price * product.quantity
    return total
