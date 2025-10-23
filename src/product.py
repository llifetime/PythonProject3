from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Union


class ZeroQuantityError(Exception):
    """Исключение для случая добавления товара с нулевым количеством"""

    def __init__(self, message: str = "Нельзя добавить товар с нулевым количеством"):
        super().__init__(message)


def _format_arguments(args: tuple, kwargs: dict) -> str:
    """Форматирует аргументы для красивого вывода"""

    def format_value(value: Any) -> str:
        return f"'{value}'" if isinstance(value, str) else str(value)

    parts = [format_value(arg) for arg in args]
    parts.extend(f"{key}={format_value(value)}" for key, value in kwargs.items())

    return ", ".join(parts)


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def _log_creation_after_init(self) -> None:
        """Логирует информацию о создании объекта после инициализации"""
        args_str = _format_arguments(self._log_args, self._log_kwargs)
        print(f"Создан объект {self._log_class_name}({args_str})")

    def __init_subclass__(cls, **kwargs):
        """Автоматически добавляет логирование в дочерние классы"""
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            self._log_class_name = self.__class__.__name__
            self._log_args = args
            self._log_kwargs = kwargs
            original_init(self, *args, **kwargs)
            self._log_creation_after_init()

        cls.__init__ = new_init


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    def __init__(self, name: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.created_at = datetime.now()

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def calculate_total_value(self) -> float:
        pass

    def apply_discount(self, discount_percent: float) -> None:
        """Применяет скидку к продукту"""
        if 0 <= discount_percent <= 100:
            self.price *= (1 - discount_percent / 100)

    def increase_quantity(self, amount: int) -> None:
        """Увеличивает количество продукта"""
        if amount > 0:
            self.quantity += amount

    def decrease_quantity(self, amount: int) -> bool:
        """Уменьшает количество продукта"""
        return (0 < amount <= self.quantity) and (self.quantity - amount >= 0)

    def is_available(self) -> bool:
        """Проверяет доступность продукта"""
        return self.quantity > 0

    def get_product_info(self) -> Dict[str, Any]:
        """Возвращает основную информацию о продукте"""
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'total_value': self.calculate_total_value(),
            'is_available': self.is_available(),
            'created_at': self.created_at
        }

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f} (Остаток: {self.quantity})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}', {self.price}, {self.quantity})"


class Product(LoggingMixin, BaseProduct):
    """Конкретный класс продукта"""

    def __init__(self, name: str, price: float, quantity: int, description: str = ""):
        super().__init__(name, price, quantity)
        self.description = description

    def get_description(self) -> str:
        return self.description or f"Продукт: {self.name}"

    def calculate_total_value(self) -> float:
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        if not isinstance(other, Product):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.calculate_total_value() + other.calculate_total_value()


class Smartphone(Product):
    """Класс Смартфон"""

    def __init__(self, name: str, price: float, quantity: int,
                 model: str, storage: int, color: str):
        description = f"Смартфон {model}, {storage}ГБ, {color}"
        super().__init__(name, price, quantity, description)
        self.model = model
        self.storage = storage
        self.color = color

    def get_tech_specs(self) -> Dict[str, Any]:
        return {
            'model': self.model,
            'storage': self.storage,
            'color': self.color
        }


class LawnGrass(Product):
    """Класс Трава газонная"""

    def __init__(self, name: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        description = f"Газонная трава из {country}, {color}, прорастание: {germination_period}"
        super().__init__(name, price, quantity, description)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_growing_info(self) -> Dict[str, Any]:
        return {
            'country': self.country,
            'germination_period': self.germination_period,
            'color': self.color
        }


class Category:
    """Класс для категорий продуктов"""

    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str, products: List[Product] = None):
        self.name = name
        self.description = description
        self.__products: List[Product] = []
        Category.total_categories += 1

        if products:
            for product in products:
                self.add_product(product)

    def _validate_product(self, product: Any) -> None:
        """Валидирует продукт перед добавлением"""
        required_attrs = ['name', 'price', 'quantity', 'get_description']
        if not all(hasattr(product, attr) for attr in required_attrs):
            raise TypeError("Можно добавлять только объекты, которые являются продуктами")

        if product.quantity == 0:
            raise ZeroQuantityError(f"Товар '{product.name}' не может быть добавлен с нулевым количеством")

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию"""
        try:
            print(f"Попытка добавления товара: {getattr(product, 'name', 'Неизвестный товар')}")

            self._validate_product(product)
            self.__products.append(product)
            Category.total_unique_products = len(self.get_products())
            print(f"Товар '{product.name}' успешно добавлен в категорию '{self.name}'")

        except (ZeroQuantityError, TypeError) as e:
            print(f"Ошибка при добавлении товара: {e}")
            raise
        finally:
            print("Обработка добавления товара завершена\n")

    def get_products(self) -> List[Product]:
        return self.__products

    @property
    def products(self) -> List[Product]:
        return self.__products

    @property
    def products_count(self) -> int:
        return len(self.__products)

    def calculate_average_price(self) -> float:
        """Подсчитывает средний ценник всех товаров в категории"""
        if not self.__products:
            return 0.0
        return sum(product.price for product in self.__products) / len(self.__products)

    def __str__(self) -> str:
        products_str = "\n".join(str(product) for product in self.__products)
        return f"Категория: {self.name}\nОписание: {self.description}\nПродукты:\n{products_str}"

    def __len__(self) -> int:
        return len(self.__products)


class Order:
    """Класс для заказов"""

    def __init__(self):
        self.__products: List[Product] = []

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в заказ"""
        try:
            print(f"Попытка добавления товара в заказ: {getattr(product, 'name', 'Неизвестный товар')}")

            if hasattr(product, 'quantity') and product.quantity == 0:
                raise ZeroQuantityError(f"Товар '{product.name}' не может быть добавлен в заказ с нулевым количеством")

            self.__products.append(product)
            print(f"Товар '{product.name}' успешно добавлен в заказ")

        except ZeroQuantityError as e:
            print(f"Ошибка при добавлении товара в заказ: {e}")
            raise
        finally:
            print("Обработка добавления товара в заказ завершена\n")

    def get_products(self) -> List[Product]:
        return self.__products


# Демонстрация работы
if __name__ == "__main__":
    def demo() -> None:
        """Демонстрация работы классов"""
        print("=== Демонстрация работы системы ===\n")

        # Тестирование исключений
        test_cases = [
            ("Создание товара с нулевым количеством",
             lambda: Product("Недоступный товар", 100, 0)),
            ("Создание смартфона с нулевым количеством",
             lambda: Smartphone("iPhone", 999, 0, "15 Pro", 256, "Black")),
            ("Создание газонной травы с нулевым количеством",
             lambda: LawnGrass("Газонная трава", 50, 0, "Германия", "14 дней", "Зеленая"))
        ]

        for test_name, test_func in test_cases:
            try:
                print(f"{test_name}:")
                test_func()
            except ValueError as e:
                print(f"   Ошибка: {e}\n")

        # Нормальная работа
        try:
            products = [
                Product("Телефон", 500, 10),
                Product("Ноутбук", 1000, 5),
                Smartphone("Samsung", 800, 3, "Galaxy", 128, "Blue"),
                LawnGrass("Premium Grass", 45, 20, "USA", "10 дней", "Green")
            ]

            electronics = Category("Электроника", "Техника и гаджеты", products[:3])
            garden = Category("Сад", "Товары для сада", [products[3]])

            order = Order()
            order.add_product(products[0])

            print("Успешные операции:")
            print(f"Категория '{electronics.name}': {len(electronics)} товаров")
            print(f"Средняя цена: {electronics.calculate_average_price():.2f} руб.")
            print(f"Заказ создан: {len(order.get_products())} товаров")

        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
