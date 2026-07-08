import json
from pathlib import Path


DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"
SALES_FILE = DATA_DIR / "sales.json"


def ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PRODUCTS_FILE.touch(exist_ok=True)
    SALES_FILE.touch(exist_ok=True)

    if PRODUCTS_FILE.read_text(encoding="utf-8").strip() == "":
        PRODUCTS_FILE.write_text("[]", encoding="utf-8")
    if SALES_FILE.read_text(encoding="utf-8").strip() == "":
        SALES_FILE.write_text("[]", encoding="utf-8")


def _read_json(path: Path) -> list:
    ensure_data_files()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _write_json(path: Path, data: list) -> None:
    ensure_data_files()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def save_products(products: list) -> None:
    _write_json(PRODUCTS_FILE, products)


def load_products() -> list:
    return _read_json(PRODUCTS_FILE)


def save_sales(sales: list) -> None:
    _write_json(SALES_FILE, sales)


def load_sales() -> list:
    return _read_json(SALES_FILE)
