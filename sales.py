from datetime import datetime

from products import find_product_by_barcode


def add_to_cart(products: list, cart: list, barcode: str) -> dict:
    product = find_product_by_barcode(products, barcode)
    if product is None:
        raise ValueError("Товар не знайдено")
    if product["quantity"] <= 0:
        raise ValueError("Товар закінчився")

    cart_item = next((item for item in cart if item["barcode"] == product["barcode"]), None)
    if cart_item:
        if cart_item["quantity"] >= product["quantity"]:
            raise ValueError("Недостатньо товару на складі")
        cart_item["quantity"] += 1
        cart_item["sum"] = cart_item["quantity"] * cart_item["price"]
        return cart_item

    cart_item = {
        "name": product["name"],
        "price": product["price"],
        "quantity": 1,
        "sum": product["price"],
        "barcode": product["barcode"],
    }
    cart.append(cart_item)
    return cart_item


def remove_from_cart(cart: list, barcode: str) -> None:
    cart_item = next((item for item in cart if item["barcode"] == barcode), None)
    if cart_item is None:
        return

    cart_item["quantity"] -= 1
    if cart_item["quantity"] <= 0:
        cart.remove(cart_item)
    else:
        cart_item["sum"] = cart_item["quantity"] * cart_item["price"]


def calculate_total(cart: list, discount_percent: float = 0) -> float:
    total = sum(item["sum"] for item in cart)
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Знижка має бути від 0 до 100")
    return round(total * (1 - discount_percent / 100), 2)


def finish_sale(products: list, cart: list, sales_history: list, discount_percent: float = 0) -> dict:
    if not cart:
        raise ValueError("Чек порожній")

    for item in cart:
        product = find_product_by_barcode(products, item["barcode"])
        if product is None or product["quantity"] < item["quantity"]:
            raise ValueError(f"Недостатньо товару: {item['name']}")

    for item in cart:
        product = find_product_by_barcode(products, item["barcode"])
        product["quantity"] -= item["quantity"]

    sale = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": calculate_total(cart, discount_percent),
        "items_count": sum(item["quantity"] for item in cart),
        "discount_percent": discount_percent,
        "items": [item.copy() for item in cart],
    }
    sales_history.append(sale)
    cart.clear()
    return sale
