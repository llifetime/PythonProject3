class Product:
    def __init__(self, name, price, quantity):
        """
        Конструктор класса Product
        """
        self.name = name
        self.__price = price  # ПРИВАТНАЯ цена
        self.quantity = quantity
    
    # Геттер для цены
    @property
    def price(self):
        """Возвращает текущую цену товара"""
        return self.__price
    
    # Сеттер для цены с проверкой
    @price.setter
    def price(self, new_price):
        """Устанавливает новую цену с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price
    
    def __str__(self):
        """Строковое представление товара"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Реализация сложения продуктов.
        Возвращает общую стоимость всех товаров на складе.
        Логика: (цена1 × количество1) + (цена2 × количество2)
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return self.price * self.quantity + other.price * other.quantity


class Category:
    def __init__(self, name):
        """
        Конструктор класса Category
        """
        self.products_list = None
        self.name = name
        self.__products = []  # ПРИВАТНЫЙ список товаров
    
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
        if not self.__products:
            return "В категории нет товаров"
        
        result = []
        for product in self.__products:
            product_info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            result.append(product_info)
        
        return "\n".join(str(product) for product in self.products)
    
    def __str__(self):
        """
        Строковое представление категории в формате:
        "Название категории, количество продуктов: 200 шт."
        """
        total_products = len(self.products)
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