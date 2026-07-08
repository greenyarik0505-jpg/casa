def validate_product(name: str, price, quantity, barcode: str) -> tuple[float, int, str, str]:
    name = (name or "").strip()
    barcode = (barcode or "").strip()

    if not name:
        raise ValueError("Назва товару не може бути порожньою")

    try:
        price = float(price)
    except (TypeError, ValueError) as exc:
        raise ValueError("Ціна повинна бути числом") from exc

    if price <= 0:
        raise ValueError("Ціна повинна бути більшою за 0")

    try:
        quantity_float = float(quantity)
        if not quantity_float.is_integer():
            raise ValueError()
        quantity = int(quantity_float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Кількість повинна бути цілим числом") from exc

    if quantity < 0:
        raise ValueError("Кількість не може бути від'ємною")

    if not barcode:
        raise ValueError("Штрихкод не може бути порожнім")

    if not barcode.isdigit() or len(barcode) != 13:
        raise ValueError("Штрихкод повинен містити 13 цифр")

    return price, quantity, name, barcode


def add_product(products: list, name: str, price, quantity, barcode: str) -> list:
    price, quantity, name, barcode = validate_product(name, price, quantity, barcode)

    if find_product_by_barcode(products, barcode) is not None:
        raise ValueError(f"Товар зі штрихкодом {barcode} вже існує")

    products.append(
        {
            "name": name,
            "price": price,
            "quantity": quantity,
            "barcode": barcode,
        }
    )
    return products


def find_product_by_barcode(products: list, barcode: str) -> dict | None:
    barcode = (barcode or "").strip()
    for product in products:
        if str(product.get("barcode", "")).strip() == barcode:
            return product
    return None
