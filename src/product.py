from abc import ABC, abstractmethod
from datetime import datetime


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
        """
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
