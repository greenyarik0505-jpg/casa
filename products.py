from barcode_tools import create_barcode_image, generate_barcode_number


def validate_product(name: str, price, quantity) -> tuple[float, int]:
    if not name.strip():
        raise ValueError("Назва товару обов'язкова")

    try:
        price = float(price)
    except ValueError as exc:
        raise ValueError("Ціна має бути числом") from exc

    try:
        quantity = int(quantity)
    except ValueError as exc:
        raise ValueError("Кількість має бути цілим числом") from exc

    if price <= 0:
        raise ValueError("Ціна має бути більшою за 0")
    if quantity < 0:
        raise ValueError("Кількість не може бути від'ємною")

    return price, quantity


def add_product(products: list, name: str, price, quantity, barcode: str | None = None) -> dict:
    price, quantity = validate_product(name, price, quantity)
    existing_barcodes = {product["barcode"] for product in products}
    barcode = barcode.strip() if barcode else generate_barcode_number(existing_barcodes)

    if barcode in existing_barcodes:
        raise ValueError("Товар з таким штрихкодом вже існує")

    image_path = create_barcode_image(barcode)
    product = {
        "name": name.strip(),
        "price": price,
        "quantity": quantity,
        "barcode": barcode,
        "barcode_image": image_path,
    }
    products.append(product)
    return product


def find_product_by_barcode(products: list, barcode: str) -> dict | None:
    barcode = barcode.strip()
    return next((product for product in products if product["barcode"] == barcode), None)
