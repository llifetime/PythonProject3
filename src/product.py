class Product:
    def __init__(self, name, description, price, quantity):
        """
        Конструктор класса Product
        """
        self.name = name
        self.__price = price  # ПРИВАТНАЯ цена
        self.quantity = quantity
        self.description = description

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
        return f"{self.name} ({self.description}), {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if isinstance(other, Product):
            # Product + Product = сумма стоимостей
            return self.price * self.quantity + other.price * other.quantity
        elif isinstance(other, (int, float)):
            # Product + число = стоимость продукта + число
            return self.price * self.quantity + other
        else:
            raise TypeError("Можно складывать только с Product или числами")

    def __radd__(self, other):
        # число + Product = число + стоимость продукта
        if isinstance(other, (int, float)):
            return other + self.price * self.quantity
        else:
            raise TypeError("Можно складывать только с числами")

    def __repr__(self):
        return f"Product('{self.name}', {self.price}, {self.quantity})"
