import random
from pathlib import Path


BARCODE_DIR = Path("barcodes")
COUNTRY_PREFIX = "482"


def _ean13_check_digit(first_12_digits: str) -> str:
    odd_sum = sum(int(digit) for digit in first_12_digits[::2])
    even_sum = sum(int(digit) for digit in first_12_digits[1::2])
    total = odd_sum + even_sum * 3
    return str((10 - total % 10) % 10)


def generate_barcode_number(existing_barcodes=None) -> str:
    existing_barcodes = set(existing_barcodes or [])

    while True:
        first_12 = COUNTRY_PREFIX + "".join(str(random.randint(0, 9)) for _ in range(9))
        barcode = first_12 + _ean13_check_digit(first_12)
        if barcode not in existing_barcodes:
            return barcode


def create_barcode_image(barcode_number: str, output_dir=BARCODE_DIR) -> str:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{barcode_number}.png"

    try:
        from barcode import EAN13
        from barcode.writer import ImageWriter

        code = EAN13(barcode_number[:12], writer=ImageWriter())
        generated_path = code.save(str(output_path.with_suffix("")))
        return generated_path
    except ImportError:
        output_path.write_text(
            "Install python-barcode and pillow to generate a real barcode image.\n",
            encoding="utf-8",
        )
        return str(output_path)
