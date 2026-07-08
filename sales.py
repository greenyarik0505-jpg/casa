from datetime import datetime

def add_to_cart(cart: list, product: dict, quantity: int = 1) -> list:
    """
    Додає товар до кошика з перевіркою залишків на складі.
    Кожен елемент кошика: {"barcode": str, "name": str, "price": float, "quantity": int, "subtotal": float}
    """
    # Шукаємо чи є цей товар вже у кошику
    existing_item = None
    for item in cart:
        if item["barcode"] == product["barcode"]:
            existing_item = item
            break

    current_cart_qty = existing_item["quantity"] if existing_item else 0
    
    # Перевірка залишків на складі
    if current_cart_qty + quantity > product["quantity"]:
        raise ValueError(
            f"Недостатньо товару '{product['name']}' на складі. "
            f"Доступно: {product['quantity']}, у чеку: {current_cart_qty}"
        )

    if existing_item:
        existing_item["quantity"] += quantity
        existing_item["subtotal"] = round(existing_item["quantity"] * existing_item["price"], 2)
    else:
        cart.append({
            "barcode": product["barcode"],
            "name": product["name"],
            "price": float(product["price"]),
            "quantity": quantity,
            "subtotal": round(float(product["price"]) * quantity, 2)
        })
    return cart


def remove_from_cart(cart: list, barcode: str) -> list:
    """
    Повністю видаляє товар з кошика за штрихкодом.
    """
    return [item for item in cart if item["barcode"] != barcode]


def calculate_total(cart: list, discount_percent: float = 0.0) -> tuple[float, float, float]:
    """
    Розраховує суму без знижки, розмір знижки та фінальну суму.
    Повертає кортеж: (subtotal, discount_amount, total)
    """
    subtotal = round(sum(item["subtotal"] for item in cart), 2)
    
    if not (0.0 <= discount_percent <= 100.0):
        raise ValueError("Знижка повинна бути в межах від 0% до 100%")
        
    discount_amount = round(subtotal * (discount_percent / 100.0), 2)
    total = round(subtotal - discount_amount, 2)
    return subtotal, discount_amount, total


def finish_sale(products: list, cart: list, sales_history: list, discount_percent: float = 0.0) -> tuple[list, list, dict]:
    """
    Завершує продаж:
    1. Списує кількість проданих товарів зі складу.
    2. Формує запис про транзакцію.
    3. Додає транзакцію в історію продажів.
    Повертає: (оновлені_товари, оновлена_історія, запис_транзакції)
    """
    if not cart:
        raise ValueError("Кошик порожній, неможливо завершити продаж")

    subtotal, discount_amount, total = calculate_total(cart, discount_percent)

    # Зменшуємо залишки на складі
    for cart_item in cart:
        product_found = False
        for p in products:
            if p["barcode"] == cart_item["barcode"]:
                if p["quantity"] < cart_item["quantity"]:
                    raise ValueError(
                        f"Помилка списання: недостатньо товару '{p['name']}' на складі. "
                        f"Доступно: {p['quantity']}, потрібно: {cart_item['quantity']}"
                    )
                p["quantity"] -= cart_item["quantity"]
                product_found = True
                break
        if not product_found:
            raise ValueError(f"Товар зі штрихкодом {cart_item['barcode']} не знайдено в базі даних")

    # Створюємо запис про продаж
    sale_record = {
        "id": len(sales_history) + 1,
        "timestamp": datetime.now().isoformat(),
        "items": cart.copy(),
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "total": total
    }

    sales_history.append(sale_record)
    return products, sales_history, sale_record

