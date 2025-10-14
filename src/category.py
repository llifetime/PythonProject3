class Category:
    """Класс для категорий продуктов"""

    # Статическая переменная для подсчета общего количества категорий
    total_categories = 0
    # Статическая переменная для подсчета общего количества уникальных продуктов
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
        self.__products = []  # Приватный атрибут для хранения продуктов
        Category.total_categories += 1

        # Добавляем продукты, если они переданы
        if products is not None:
            for product in products:
                self.add_product(product)

    def add_product(self, product) -> None:
        """
        Добавляет продукт в категорию

        Args:
            product: Продукт для добавления (объект класса Product или его наследников)
        """
        # Проверяем, что продукт имеет необходимые атрибуты вместо проверки типа
        if (hasattr(product, "name")
                and hasattr(product, 'price')
                and hasattr(product, 'quantity')
                and hasattr(product, 'get_description')):
            self.__products.append(product)
            # Обновляем счетчик уникальных продуктов
            Category.total_unique_products = len(self.get_products())
        else:
            raise TypeError("Можно добавлять только объекты, которые являются продуктами")

    def get_products(self) -> list:
        """
        Возвращает список продуктов в категории

        Returns:
            list: Список продуктов
        """
        return self.__products

    @property
    def products(self) -> list:
        """
        Свойство для доступа к списку продуктов

        Returns:
            list: Список продуктов
        """
        return self.__products

    @property
    def products_count(self) -> int:
        """
        Возвращает количество продуктов в категории

        Returns:
            int: Количество продуктов
        """
        return len(self.__products)

    @property
    def category_count(self) -> int:
        """
        Возвращает общее количество категорий (статическое свойство)

        Returns:
            int: Общее количество категорий
        """
        return Category.total_categories

    def get_products_info(self) -> list:
        """
        Возвращает информацию о всех продуктах в категории

        Returns:
            list: Список с информацией о продуктах
        """
        return [self._get_product_info(product) for product in self.__products]

    def _get_product_info(self, product) -> dict:
        """
        Вспомогательный метод для получения информации о продукте

        Args:
            product: Продукт для получения информации

        Returns:
            dict: Информация о продукте
        """
        info = {
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'description': product.get_description() if hasattr(product, 'get_description') else "",
            'is_available': product.quantity > 0 if hasattr(product, 'quantity') else False
        }

        # Добавляем total_value если продукт имеет метод calculate_total_value
        if hasattr(product, 'calculate_total_value'):
            info['total_value'] = product.calculate_total_value()

        return info

    def __str__(self) -> str:
        """Строковое представление категории"""
        products_info = []
        for product in self.__products:
            # Используем строковое представление продукта
            product_str = str(product)
            products_info.append(product_str)

        products_str = "\n".join(products_info)
        return f"Категория: {self.name}\nОписание: {self.description}\nПродукты:\n{products_str}"

    def __len__(self) -> int:
        """Возвращает количество продуктов в категории"""
        return len(self.__products)
