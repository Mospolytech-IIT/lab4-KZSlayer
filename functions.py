"""Module providing core functions for warehouse operations with exception handling."""

# Список для хранения товаров на складе
inventory = {}

# Пользовательские исключения с логикой
class InvalidQuantityError(Exception):
    """Raised when the quantity provided is invalid (e.g., negative or zero)."""

    def __init__(self, quantity, message="Недопустимое количество товара"):
        self.quantity = quantity
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.quantity}. Количество должно быть больше нуля."

class InvalidPriceError(Exception):
    """Raised when the price provided is invalid (e.g., negative)."""

    def __init__(self, price, message="Недопустимая цена товара"):
        self.price = price
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.price}. Цена должна быть неотрицательной."

class ItemNotFoundError(Exception):
    """Raised when the requested item is not found in the inventory."""

    def __init__(self, item_name, message="Товар не найден"):
        self.item_name = item_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: '{self.item_name}'. Проверьте правильность ввода или наличие товара."

def greet():
    """Displays a welcome message for the inventory management system."""
    print("Добро пожаловать в систему управления складом!")

# 1. Функции, которые выбрасывают исключения при определённых значениях входных параметров.
def add_item(name, quantity=1, price=0.0):
    """
    Adds a new item to the inventory or updates an existing item.
    Raises an exception if quantity or price is invalid.
    """
    if quantity <= 0:
        raise InvalidQuantityError(quantity)
    if price < 0:
        raise InvalidPriceError(price)
    if name in inventory:
        inventory[name]['quantity'] += quantity
        inventory[name]['price'] = price
    else:
        inventory[name] = {'quantity': quantity, 'price': price}
    return f"Товар '{name}' добавлен на склад: {quantity} шт. по цене {price} за штуку."

def calculate_total(price, quantity):
    """Calculates and returns the total cost for an item based on price and quantity."""
    if price < 0:
        raise InvalidPriceError(price)
    if quantity < 0:
        raise InvalidQuantityError(quantity)
    return price * quantity

# 2. Функция с общим обработчиком исключений
def display_item_details(name):
    """Displays details of an item, raises ItemNotFoundError if item not found."""
    try:
        item = inventory[name]
        details = f"{name}: {item['quantity']} шт. по {item['price']} за шт."
        print(details)
        return details
    except Exception as e:
        print(f"Ошибка при получении данных о товаре: {e}")
        return f"Товар '{name}' не найден."

# 3. Функция с обработчиком общего типа и блоком finally
def update_item(name, quantity=None, price=None):
    """
    Updates item information in the inventory with provided keyword arguments.
    """
    try:
        if name not in inventory:
            raise ItemNotFoundError(name)
        if quantity is not None and quantity < 0:
            raise InvalidQuantityError(quantity)
        if price is not None and price < 0:
            raise InvalidPriceError(price)

        if quantity is not None:
            inventory[name]['quantity'] = quantity
        if price is not None:
            inventory[name]['price'] = price
        updates = f"{name}: quantity={inventory[name]['quantity']}, price={inventory[name]['price']}"
        return updates
    except Exception as e:
        print(f"Ошибка при обновлении товара '{name}': {e}")
    finally:
        print(f"Завершено обновление информации о товаре '{name}'.")

# 4. Функция с обработкой различных типов исключений и блоком finally
def apply_discount(name, discount_percentage):
    """
    Applies a discount to the price of an item in the inventory.
    Raises exceptions for invalid discount or item not found.
    """
    try:
        if name not in inventory:
            raise ItemNotFoundError(name)
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Скидка должна быть в диапазоне от 0 до 100.")
        original_price = inventory[name]['price']
        discount_rate = discount_percentage / 100
        discounted_price = original_price * (1 - discount_rate)
        if discounted_price < 0:
            raise ArithmeticError("Расчёт скидки привёл к отрицательной цене.")
        inventory[name]['price'] = discounted_price
        return f"Новая цена товара '{name}' со скидкой: {discounted_price}"
    except ItemNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except ArithmeticError as e:
        print(f"Ошибка вычисления: {e}")
    finally:
        print(f"Процедура скидки завершена для товара '{name}'.")

# 5. Функция, генерирующая исключения и обрабатывающая их
def complete_order(order_id, items):
    """
    Completes an order by processing it. Raises exceptions for invalid data.
    """
    try:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Неверный формат ID заказа.")
        if not isinstance(items, list) or not items:
            raise ValueError("Список товаров не может быть пустым.")
        for item in items:
            if item not in inventory or inventory[item]['quantity'] <= 0:
                raise ItemNotFoundError(item)
        for item in items:
            inventory[item]['quantity'] -= 1
        print(f"Заказ {order_id} успешно обработан.")
    except ValueError as e:
        print(f"Ошибка ввода данных: {e}")
    except ItemNotFoundError as e:
        print(f"Ошибка: {e}")
    finally:
        print("Процедура завершения заказа завершена.")

# 6. Пример использования пользовательских исключений
def remove_item(name, quantity):
    """
    Removes a specified quantity of an item from the inventory.
    Raises InvalidQuantityError or ItemNotFoundError if there are issues.
    """
    try:
        if name not in inventory:
            raise ItemNotFoundError(name)
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        if inventory[name]['quantity'] < quantity:
            raise InvalidQuantityError(quantity, message="Недостаточное количество на складе")
        inventory[name]['quantity'] -= quantity
        return f"Удалено {quantity} шт. товара '{name}'. Осталось на складе: {inventory[name]['quantity']} шт."
    except (ItemNotFoundError, InvalidQuantityError) as e:
        print(f"Ошибка удаления товара: {e}")
    finally:
        print(f"Операция удаления товара '{name}' завершена.")

# 7. Демонстрация работы функций с исключениями
def demo_exceptions():
    """Demonstrates exception handling in various functions."""
    try:
        add_item("Nokia 3310", -5, 100)
    except InvalidQuantityError as e:
        print(e)
    try:
        calculate_total(-10, 2)
    except InvalidPriceError as e:
        print(e)
    try:
        remove_item("Xiaomi 14", 2)
    except ItemNotFoundError as e:
        print(e)

# 7. Демонстрация работы функций с исключениями
def demo_exceptions1():
    """Demonstrates exception handling in various functions."""
    def main_menu():
        print("\n1. Добавить товар")
        print("2. Обновить товар")
        print("3. Просмотреть все товары")
        print("4. Рассчитать общую стоимость товара")
        print("5. Применить скидку")
        print("6. Завершить заказ")
        print("7. Выйти")
    greet()
    while True:
        main_menu()
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                name = input("Введите название товара: ")
                quantity = int(input("Введите количество: "))
                price = float(input("Введите цену: "))
                print(add_item(name, quantity, price))
            elif choice == "2":
                name = input("Введите название товара для обновления: ")
                quantity = input("Введите новое количество (или оставьте пустым): ")
                price = input("Введите новую цену (или оставьте пустым): ")
                updates = {}
                if quantity:
                    updates['quantity'] = int(quantity)
                if price:
                    updates['price'] = float(price)
                print(update_item(name, **updates))
            elif choice == "3":
                if inventory:
                    for item, details in inventory.items():
                        print(f"{item}: {details['quantity']} шт. по {details['price']} за шт.")
                else:
                    print("Склад пуст.")
            elif choice == "4":
                name = input("Введите название товара: ")
                if name in inventory:
                    price = inventory[name]['price']
                    quantity = inventory[name]['quantity']
                    total_cost = calculate_total(price, quantity)
                    print(f"Общая стоимость товара '{name}': {total_cost}")
                else:
                    print(f"Товар '{name}' не найден на складе.")
            elif choice == "5":
                name = input("Введите название товара для скидки: ")
                discount_percentage = float(input("Введите размер скидки в процентах: "))
                print(apply_discount(name, discount_percentage))
            elif choice == "6":
                order_id = input("Введите ID заказа: ")
                items = input("Введите список товаров через запятую: ").split(',')
                items = [item.strip() for item in items]
                print(complete_order(order_id, items))
            elif choice == "7":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
