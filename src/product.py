from abc import ABC, abstractmethod
from datetime import datetime


class ZeroQuantityError(Exception):
    """Исключение для случая добавления товара с нулевым количеством"""

    def __init__(self, message="Нельзя добавить товар с нулевым количеством"):
        self.message = message
        super().__init__(self.message)


def _format_arguments(args, kwargs) -> str:
    """Форматирует аргументы для красивого вывода"""
    parts = []

    # Добавляем позиционные аргументы
    for arg in args:
        if isinstance(arg, str):
            parts.append(f"'{arg}'")
        else:
            parts.append(str(arg))

    # Добавляем именованные аргументы
    for key, value in kwargs.items():
        if isinstance(value, str):
            parts.append(f"{key}='{value}'")
        else:
            parts.append(f"{key}={value}")

    return ", ".join(parts)


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        """
        Инициализация с логированием

        Args:
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы
        """
        # Сохраняем информацию для логирования
        self._log_class_name = self.__class__.__name__
        self._log_args = args
        self._log_kwargs = kwargs

        # Вызываем __init__ следующего класса в MRO
        super().__init__(*args, **kwargs)

        # Логируем после инициализации
        self._log_creation_after_init()

    def _log_creation_after_init(self):
        """Логирует информацию о создании объекта после инициализации"""
        args_str = _format_arguments(self._log_args, self._log_kwargs)
        print(f"Создан объект {self._log_class_name}({args_str})")


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    def __init__(self, name: str, price: float, quantity: int):
        """
        Инициализация продукта

        Args:
            name (str): Название продукта
            price (float): Цена продукта
            quantity (int): Количество продукта

        Raises:
            ValueError: Если quantity равно 0
        """
        # Проверка количества при создании товара
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.created_at = datetime.now()

    @abstractmethod
    def get_description(self) -> str:
        """Абстрактный метод для получения описания продукта"""
        pass

    @abstractmethod
    def calculate_total_value(self) -> float:
        """Абстрактный метод для расчета общей стоимости"""
        pass

    def apply_discount(self, discount_percent: float) -> None:
        """
        Применяет скидку к продукту

        Args:
            discount_percent (float): Процент скидки (0-100)
        """
        if 0 <= discount_percent <= 100:
            self.price *= (1 - discount_percent / 100)

    def increase_quantity(self, amount: int) -> None:
        """
        Увеличивает количество продукта

        Args:
            amount (int): Количество для добавления
        """
        if amount > 0:
            self.quantity += amount

    def decrease_quantity(self, amount: int) -> bool:
        """
        Уменьшает количество продукта

        Args:
            amount (int): Количество для уменьшения

        Returns:
            bool: True если операция успешна, False если недостаточно товара
        """
        if 0 < amount <= self.quantity:
            self.quantity -= amount
            return True
        return False

    def is_available(self) -> bool:
        """
        Проверяет доступность продукта

        Returns:
            bool: True если продукт доступен (количество > 0)
        """
        return self.quantity > 0

    def get_product_info(self) -> dict:
        """
        Возвращает основную информацию о продукте

        Returns:
            dict: Словарь с информацией о продукте
        """
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'total_value': self.calculate_total_value(),
            'is_available': self.is_available(),
            'created_at': self.created_at
        }

    def __str__(self) -> str:
        """Строковое представление продукта"""
        return f"{self.name} - ${self.price:.2f} (Остаток: {self.quantity})"

    def __repr__(self) -> str:
        """Представление для разработчика"""
        return f"{self.__class__.__name__}('{self.name}', {self.price}, {self.quantity})"


class Product(LoggingMixin, BaseProduct):
    """Конкретный класс продукта, наследующий от BaseProduct с логированием"""

    def __init__(self, name: str, price: float, quantity: int, description: str = ""):
        """
        Инициализация продукта с логированием

        Args:
            name (str): Название продукта
            price (float): Цена продукта
            quantity (int): Количество продукта
            description (str): Описание продукта (по умолчанию пустая строка)

        Raises:
            ValueError: Если quantity равно 0
        """
        # Вызываем __init__ миксина, который залогирует создание и вызовет BaseProduct.__init__
        super().__init__(name, price, quantity)
        # Инициализируем специфичные для Product атрибуты
        self.description = description

    def get_description(self) -> str:
        """Возвращает описание продукта"""
        return self.description or f"Продукт: {self.name}"

    def calculate_total_value(self) -> float:
        """Рассчитывает общую стоимость всех единиц продукта"""
        return self.price * self.quantity

    def __str__(self) -> str:
        """Строковое представление продукта в формате: Название, цена руб. Остаток: количество шт."""
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Сложение двух продуктов. Возвращает общую стоимость всех единиц товара.

        Args:
            other (Product): Другой продукт для сложения

        Returns:
            float: Суммарная стоимость всех единиц товара

        Raises:
            TypeError: Если other не является экземпляром Product
        """
        if not isinstance(other, Product):
            raise TypeError("Нельзя складывать товары разных типов")

        return self.calculate_total_value() + other.calculate_total_value()


class Smartphone(Product):
    """Класс Смартфон, наследующий от Product"""

    def __init__(self, name: str, price: float, quantity: int,
                 model: str, storage: int, color: str):
        """
        Инициализация смартфона

        Args:
            name (str): Название смартфона
            price (float): Цена
            quantity (int): Количество
            model (str): Модель смартфона
            storage (int): Объем памяти в ГБ
            color (str): Цвет

        Raises:
            ValueError: Если quantity равно 0
        """
        description = f"Смартфон {model}, {storage}ГБ, {color}"
        super().__init__(name, price, quantity, description)
        self.model = model
        self.storage = storage
        self.color = color

    def get_tech_specs(self) -> dict:
        """Возвращает технические характеристики"""
        return {
            'model': self.model,
            'storage': self.storage,
            'color': self.color
        }


class LawnGrass(Product):
    """Класс Трава газонная, наследующий от Product"""

    def __init__(self, name: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        """
        Инициализация газонной травы

        Args:
            name (str): Название
            price (float): Цена
            quantity (int): Количество
            country (str): Страна производства
            germination_period (str): Срок прорастания
            color (str): Цвет травы

        Raises:
            ValueError: Если quantity равно 0
        """
        description = f"Газонная трава из {country}, {color}, прорастание: {germination_period}"
        super().__init__(name, price, quantity, description)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_growing_info(self) -> dict:
        """Возвращает информацию о выращивании"""
        return {
            'country': self.country,
            'germination_period': self.germination_period,
            'color': self.color
        }


class Category:
    """Класс для категорий продуктов"""

    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str, products: list = None):
        """
        Инициализация категории

        Args:
            name (str): Название категории
            description (str): Описание категории
            products (list, optional): Список продуктов для добавления при создании
        """
        self.name = name
        self.description = description
        self.__products = []
        Category.total_categories += 1

        if products is not None:
            for product in products:
                self.add_product(product)

    def add_product(self, product) -> None:
        """
        Добавляет продукт в категорию

        Args:
            product: Продукт для добавления

        Raises:
            ZeroQuantityError: Если количество товара равно 0
            TypeError: Если объект не является продуктом
        """
        try:
            print(f"Попытка добавления товара: {getattr(product, 'name', 'Неизвестный товар')}")

            # Проверяем, что продукт имеет необходимые атрибуты
            if (hasattr(product, "name") and hasattr(product, 'price') and
                    hasattr(product, 'quantity') and hasattr(product, 'get_description')):

                # Проверяем количество товара
                if product.quantity == 0:
                    raise ZeroQuantityError(f"Товар '{product.name}' не может быть добавлен с нулевым количеством")

                self.__products.append(product)
                Category.total_unique_products = len(self.get_products())
                print(f"Товар '{product.name}' успешно добавлен в категорию '{self.name}'")

            else:
                raise TypeError("Можно добавлять только объекты, которые являются продуктами")

        except (ZeroQuantityError, TypeError) as e:
            print(f"Ошибка при добавлении товара: {e}")
            raise
        finally:
            print("Обработка добавления товара завершена\n")

    def get_products(self) -> list:
        """Возвращает список продуктов в категории"""
        return self.__products

    @property
    def products(self) -> list:
        """Свойство для доступа к списку продуктов"""
        return self.__products

    def calculate_average_price(self) -> float:
        """
        Подсчитывает средний ценник всех товаров в категории.
        Возвращает 0, если в категории нет товаров.
        """
        try:
            total_price = sum(product.price for product in self.__products)
            average = total_price / len(self.__products)
            return average
        except ZeroDivisionError:
            return 0

    def __str__(self) -> str:
        """Строковое представление категории"""
        products_info = []
        for product in self.__products:
            product_str = str(product)
            products_info.append(product_str)

        products_str = "\n".join(products_info)
        return f"Категория: {self.name}\nОписание: {self.description}\nПродукты:\n{products_str}"

    def __len__(self) -> int:
        """Возвращает количество продуктов в категории"""
        return len(self.__products)


class Order:
    """Класс для заказов"""

    def __init__(self):
        self.__products = []

    def add_product(self, product) -> None:
        """
        Добавляет продукт в заказ

        Args:
            product: Продукт для добавления

        Raises:
            ZeroQuantityError: Если количество товара равно 0
        """
        try:
            print(f"Попытка добавления товара в заказ: {getattr(product, 'name', 'Неизвестный товар')}")

            # Проверяем количество товара
            if hasattr(product, 'quantity') and product.quantity == 0:
                raise ZeroQuantityError(f"Товар '{product.name}' не может быть добавлен в заказ с нулевым количеством")

            self.__products.append(product)
            print(f"Товар '{product.name}' успешно добавлен в заказ")

        except ZeroQuantityError as e:
            print(f"Ошибка при добавлении товара в заказ: {e}")
            raise
        finally:
            print("Обработка добавления товара в заказ завершена\n")

    def get_products(self) -> list:
        """Возвращает список продуктов в заказе"""
        return self.__products


# Примеры использования с обработкой исключений
if __name__ == "__main__":
    print("=== Тестирование исключений для товаров с нулевым количеством ===\n")

    # Тестирование создания товара с нулевым количеством
    try:
        print("1. Попытка создать товар с нулевым количеством:")
        bad_product = Product("Недоступный товар", 100, 0)
    except ValueError as e:
        print(f"   Ошибка: {e}\n")

    # Создание нормальных товаров
    try:
        print("2. Создание нормальных товаров:")
        product1 = Product("Телефон", 500, 10)
        product2 = Product("Ноутбук", 1000, 5)
        print("   Товары успешно созданы\n")
    except ValueError as e:
        print(f"   Ошибка: {e}\n")

    # Создание категории и добавление товаров
    try:
        print("3. Создание категории и добавление товаров:")
        electronics = Category("Электроника", "Техника и гаджеты")
        electronics.add_product(product1)
        electronics.add_product(product2)
        print(f"   Средняя цена в категории: {electronics.calculate_average_price():.2f} руб.\n")
    except (ValueError, ZeroQuantityError) as e:
        print(f"   Ошибка: {e}\n")

    # Работа с заказом
    try:
        print("4. Работа с заказом:")
        order = Order()
        order.add_product(product1)
        print("   Заказ успешно создан\n")
    except ZeroQuantityError as e:
        print(f"   Ошибка: {e}\n")

    # Тестирование наследованных классов
    try:
        print("5. Тестирование наследованных классов:")
        smartphone = Smartphone("iPhone", 999, 0, "15 Pro", 256, "Black")
    except ValueError as e:
        print(f"   Ошибка при создании смартфона: {e}\n")

    try:
        lawn_grass = LawnGrass("Газонная трава", 50, 0, "Германия", "14 дней", "Зеленая")
    except ValueError as e:
        print(f"   Ошибка при создании газонной травы: {e}\n")