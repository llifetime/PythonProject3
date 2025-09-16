"""Main module to demonstrate Product and Category functionality."""

from product import Product, Category


def main():
    """Demonstrate Product and Category classes functionality."""
    # Create products
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14
    )

    # Display product information
    print("=== ИНФОРМАЦИЯ О ТОВАРАХ ===")
    for i, product in enumerate([product1, product2, product3], 1):
        print(f"\nТовар {i}:")
        print(f"Название: {product.name}")
        print(f"Описание: {product.description}")
        print(f"Цена: {product.price}")
        print(f"Количество: {product.quantity}")

    # Create category with products
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print("\n=== ИНФОРМАЦИЯ О КАТЕГОРИИ ===")
    print(f"Название категории: {category1.name}")
    print(f"Описание категории: {category1.description}")
    print(f"Количество товаров в категории: {len(category1.products)}")
    print(f"Всего категорий в системе: {Category.total_categories}")
    print(f"Всего уникальных товаров: {Category.total_unique_products}")

    # Display products in category
    print("\nТовары в категории:")
    for product in category1.products:
        print(f"  - {product.name}: {product.price} руб. (остаток: {product.quantity})")

    # Create another category
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, "
        "станет вашим другом и помощником",
        [product4]
    )

    print("\n=== ИНФОРМАЦИЯ О КАТЕГОРИИ ===")
    print(f"Название категории: {category2.name}")
    print(f"Описание категории: {category2.description}")
    print(f"Количество товаров в категории: {len(category2.products)}")
    print(f"Всего категорий в системе: {Category.total_categories}")
    print(f"Всего уникальных товаров: {Category.total_unique_products}")


if __name__ == "__main__":
    main()
