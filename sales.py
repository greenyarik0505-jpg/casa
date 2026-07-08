from datetime import datetime

from products import find_product_by_barcode


def add_to_cart(products: list, cart: list, barcode: str) -> dict:
    product = find_product_by_barcode(products, barcode)
    if product is None:
        raise ValueError("Товар з таким штрихкодом не знайдено")

    available = int(product.get("quantity", 0))
    if available <= 0:
        raise ValueError("Товар закінчився")

    cart_item = find_product_by_barcode(cart, barcode)
    if cart_item is not None:
        if cart_item["quantity"] >= available:
            raise ValueError("Недостатньо товару на складі")
        cart_item["quantity"] += 1
        cart_item["sum"] = round(cart_item["price"] * cart_item["quantity"], 2)
        return cart_item

    cart_item = {
        "barcode": product["barcode"],
        "name": product["name"],
        "price": float(product["price"]),
        "quantity": 1,
        "sum": round(float(product["price"]), 2),
    }
    cart.append(cart_item)
    return cart_item


def remove_from_cart(cart: list, barcode: str) -> bool:
    cart_item = find_product_by_barcode(cart, barcode)
    if cart_item is None:
        return False

    cart_item["quantity"] -= 1
    if cart_item["quantity"] <= 0:
        cart.remove(cart_item)
    else:
        cart_item["sum"] = round(cart_item["price"] * cart_item["quantity"], 2)
    return True


def calculate_total(cart: list, discount_percent=0) -> float:
    try:
        discount_percent = float(discount_percent or 0)
    except (TypeError, ValueError) as exc:
        raise ValueError("Знижка повинна бути числом") from exc

    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Знижка повинна бути від 0 до 100")

    subtotal = sum(float(item.get("sum", 0)) for item in cart)
    return round(subtotal * (1 - discount_percent / 100), 2)


def finish_sale(products: list, cart: list, sales_history: list, discount_percent=0) -> dict:
    if not cart:
        raise ValueError("Чек порожній")

    for item in cart:
        product = find_product_by_barcode(products, item["barcode"])
        if product is None:
            raise ValueError(f"Товар не знайдено: {item['name']}")
        if int(product.get("quantity", 0)) < int(item["quantity"]):
            raise ValueError(f"Недостатньо товару на складі: {item['name']}")

    for item in cart:
        product = find_product_by_barcode(products, item["barcode"])
        product["quantity"] = int(product["quantity"]) - int(item["quantity"])

    sale = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": calculate_total(cart, discount_percent),
        "items_count": sum(int(item["quantity"]) for item in cart),
        "discount_percent": float(discount_percent or 0),
        "items": [item.copy() for item in cart],
    }
    sales_history.append(sale)
    cart.clear()
    return sale
