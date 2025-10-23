from src.category import Category
from src.product import LawnGrass, Product

if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", 1000, 0, "Неверное количество")
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", 180000, 5, "256GB, Серый цвет, 200MP камера")
    product2 = Product("Iphone 15", 210000, 8, "512GB, Gray space")
    product3 = Product("Xiaomi Redmi Note 11", 31000, 14, "1024GB, Синий")

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())

    product1 = Product("Samsung Galaxy S23 Ultra", 180000, 5, "256GB, Серый цвет, 200MP камера")
    product2 = Product("Iphone 15", 210000, 8, "512GB, Gray space")
    product3 = Product("Xiaomi Redmi Note 11", 31000, 14, "1024GB, Синий")

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
    print(category1.category_count)
    print(category1.products_count)

    product4 = Product("55\" QLED 4K", 123000, 7, "Фоновая подсветка")
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.products_count)

    grass1 = LawnGrass("Элитная трава для газона", 500, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

