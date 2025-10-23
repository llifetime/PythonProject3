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
            product: Продукт для добавления

        Raises:
            ValueError: Если количество товара равно 0
        """
        try:
            print(f"Попытка добавления товара: {getattr(product, 'name', 'Неизвестный товар')}")

            # Проверяем, что продукт имеет необходимые атрибуты
            if (hasattr(product, "name") and hasattr(product, 'price') and
                    hasattr(product, 'quantity') and hasattr(product, 'get_description')):

                # ПРОВЕРКА НА НУЛЕВОЕ КОЛИЧЕСТВО - ДОБАВЬТЕ ЭТО
                if product.quantity == 0:
                    raise ValueError(f"Товар '{product.name}' не может быть добавлен с нулевым количеством")

                self.__products.append(product)
                Category.total_unique_products = len(self.get_products())
                print(f"Товар '{product.name}' успешно добавлен в категорию '{self.name}'")

            else:
                raise TypeError("Можно добавлять только объекты, которые являются продуктами")

        except (ValueError, TypeError) as e:
            print(f"Ошибка при добавлении товара: {e}")
            raise
        finally:
            print("Обработка добавления товара завершена\n")

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

    # Добавьте этот метод как псевдоним
    def middle_price(self) -> float:
        """Псевдоним для calculate_average_price"""
        return self.calculate_average_price()

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

