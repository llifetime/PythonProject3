from src.product import Product


class Category:
    def __init__(self, name, description="", products=None):
        """
        Конструктор класса Category
        """
        self.name = name
        self.__products = []  # ПРИВАТНЫЙ список товаров
        self.description = description
        self.__products = products if products is not None else []

    def add_product(self, product):
        """
        Добавляет товар в категорию с проверкой типа

        Args:
            product: Объект для добавления (должен быть Product или его подклассом)
        """
        # ПРОВЕРКА ТИПА с помощью isinstance
        if not isinstance(product, Product):
            print(f"Ошибка: можно добавлять только объекты класса Product, а получен {type(product)}")
            return False

        # Если проверка пройдена - добавляем товар
        self.__products.append(product)
        print(f"Товар '{product.name}' добавлен в категорию '{self.name}'")
        return True

    # Геттер для просмотра товаров
    @property
    def products(self):
        """Возвращает список товаров в формате строк"""
        return self.__products

    @property
    def products_list(self):
        """Возвращает строку с информацией о всех товарах"""
        if not self.__products:
            return ""

        product_strings = []
        for product in self.__products:
            product_info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            product_strings.append(product_info)

        return "\n".join(product_strings)

    def __str__(self):
        """
        Строковое представление категории в формате:
        "Название категории, количество продуктов: 200 шт."
        """
        total_products = len(self.__products)
        return f"{self.name}, количество продуктов: {total_products} шт."

    def total_value(self):
        """
        Дополнительный метод для расчета общей стоимости всех товаров в категории.
        """
        return sum(product.price * product.quantity for product in self.products)


def sum_products(*products):
    """Складывает стоимость нескольких продуктов"""
    total = 0
    for product in products:
        if not isinstance(product, Product):
            raise TypeError("Все аргументы должны быть объектами Product")
        total += product.price * product.quantity
    return total
