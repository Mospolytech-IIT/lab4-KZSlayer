"""Module that demonstrates a complete workflow for an inventory management system."""
from functions import (
    greet,
    add_item,
    calculate_total,
    display_item_details,
    update_item,
    apply_discount,
    complete_order,
    remove_item,
    demo_exceptions,
    demo_exceptions1
)

def complete_inventory_demo():
    """Функция, которая последовательно вызывает все ранее определенные функции."""
    greet()

    # Добавление товаров
    print(add_item("Samsung S24", 10, 60000))
    print(add_item("Iphone 16", 5, 100000))

    # Расчет общей стоимости
    print(calculate_total(150, 10))

    # Отображение деталей товара
    print(display_item_details("Samsung S24"))

    # Обновление информации о товаре
    print(update_item("Samsung S24", quantity=20, price=55000))

    # Применение скидки
    print(apply_discount("Samsung S24", 25))

    # Завершение заказа
    complete_order("order_123", ["Samsung S24", "Iphone 16"])

    # Удаление товаров
    print(remove_item("Samsung S24", 5))

    # Демонстрация обработки исключений
    demo_exceptions()
    demo_exceptions1()

if __name__ == "__main__":
    complete_inventory_demo()
