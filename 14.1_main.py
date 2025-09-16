class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - {self.price} руб. (в наличии: {self.quantity})"


class Category:
    # Атрибуты класса (общие для всех объектов)
    total_categories = 0
    total_unique_products = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Увеличиваем счетчик категорий
        Category.total_categories += 1

        # Увеличиваем счетчик уникальных товаров на количество товаров в этой категории
        Category.total_unique_products += len(self.products)

    def add_product(self, product):
        """Добавляет товар в категорию"""
        self.products.append(product)
        # При добавлении товара увеличиваем общий счетчик
        Category.total_unique_products += 1

    def remove_product(self, product_name):
        """Удаляет товар из категории по названию"""
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                # При удалении товара уменьшаем общий счетчик
                Category.total_unique_products -= 1
                break

    def get_total_products(self):
        """Возвращает общее количество товаров в категории"""
        return len(self.products)

    def get_total_quantity(self):
        """Возвращает общее количество всех товаров в наличии"""
        return sum(product.quantity for product in self.products)

    def __str__(self):
        return f"Категория: {self.name} ({self.get_total_products()} товаров)"


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))

    # Выводим атрибуты класса
    print(f"Всего категорий: {Category.total_categories}")
    print(f"Всего уникальных товаров: {Category.total_unique_products}")

    print("Товары в категории:")
    for product in category1.products:
        print(f"  - {product.name}: {product.price} руб. (остаток: {product.quantity})")

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))

    # Выводим обновленные атрибуты класса
    print(f"Всего категорий: {Category.total_categories}")
    print(f"Всего уникальных товаров: {Category.total_unique_products}")

    print("Товары в категории:")
    for product in category2.products:
        print(f"  - {product.name}: {product.price} руб. (остаток: {product.quantity})")