class Product:
    """Базовый класс для товаров"""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, value):
        """Сеттер для цены с проверкой"""
        if value <= 0:
            print("Цена не должна быть нулевой или отрицательной")
        else:
            self.__price = value

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"

    def __add__(self, other):
        """Метод для сложения товаров (общая стоимость)"""
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Класс для смартфонов"""

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"Смартфон {self.name} ({self.model}), {self.color}, {self.memory}GB, {self.price} руб."

    def __repr__(self):
        return (
            f"Smartphone({self.name}, {self.description}, {self.price}, "
            f"{self.quantity}, {self.efficiency}, {self.model}, {self.memory}, {self.color})"
        )


class LawnGrass(Product):
    """Класс для газонной травы"""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"Газонная трава {self.name}, {self.color}, {self.country}, {self.price} руб."

    def __repr__(self):
        return (
            f"LawnGrass({self.name}, {self.description}, {self.price}, "
            f"{self.quantity}, {self.country}, {self.germination_period}, {self.color})"
        )
