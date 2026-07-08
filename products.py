def add_product(products: list, name: str, price: float, quantity: int, barcode: str) -> list:
    if not name or not name.strip():
        raise ValueError("Назва товару не може бути порожньою")
    try:
        price = float(price)
        if price < 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Ціна повинна бути невід'ємним числом")
        
    try:
        # Перевірка на дробові числа (float або рядки з крапкою)
        if isinstance(quantity, float):
            if not quantity.is_integer():
                raise ValueError()
            quantity = int(quantity)
        elif isinstance(quantity, str) and "." in quantity:
            # Спроба розпарсити як float і перевірити чи воно ціле
            f_val = float(quantity)
            if not f_val.is_integer():
                raise ValueError()
            quantity = int(f_val)
        else:
            quantity = int(quantity)
            
        if quantity < 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Кількість повинна бути невід'ємним цілим числом")

    if not barcode or not barcode.strip():
        raise ValueError("Штрихкод не може бути порожнім")
    
    # Перевірка унікальності штрихкоду
    for product in products:
        if product["barcode"] == barcode:
            raise ValueError(f"Товар зі штрихкодом {barcode} вже існує")
            
    products.append({
        "name": name.strip(),
        "price": price,
        "quantity": quantity,
        "barcode": barcode.strip()
    })
    return products


def find_product_by_barcode(products: list, barcode: str) -> dict | None:
    for product in products:
        if product["barcode"] == barcode:
            return product
    return None

