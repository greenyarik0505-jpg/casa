import unittest
from products import add_product, find_product_by_barcode

class TestProducts(unittest.TestCase):
    def setUp(self):
        self.products = [
            {"name": "Молоко", "price": 32.50, "quantity": 10, "barcode": "4820001111111"},
            {"name": "Хліб", "price": 18.00, "quantity": 5, "barcode": "4820002222222"}
        ]

    def test_add_product_success(self):
        initial_len = len(self.products)
        updated = add_product(self.products, "Масло", 65.90, 8, "4820003333333")
        self.assertEqual(len(updated), initial_len + 1)
        self.assertEqual(updated[-1]["name"], "Масло")
        self.assertEqual(updated[-1]["price"], 65.90)
        self.assertEqual(updated[-1]["quantity"], 8)
        self.assertEqual(updated[-1]["barcode"], "4820003333333")

    def test_add_product_duplicate_barcode(self):
        with self.assertRaises(ValueError) as context:
            add_product(self.products, "Ще одне молоко", 35.00, 2, "4820001111111")
        self.assertIn("вже існує", str(context.exception))

    def test_add_product_empty_name(self):
        with self.assertRaises(ValueError):
            add_product(self.products, "", 10.0, 5, "4820003333333")
        with self.assertRaises(ValueError):
            add_product(self.products, "   ", 10.0, 5, "4820003333333")

    def test_add_product_invalid_price(self):
        with self.assertRaises(ValueError):
            add_product(self.products, "Товар", -5.0, 5, "4820003333333")
        with self.assertRaises(ValueError):
            add_product(self.products, "Товар", "безкоштовно", 5, "4820003333333")

    def test_add_product_invalid_quantity(self):
        with self.assertRaises(ValueError):
            add_product(self.products, "Товар", 10.0, -1, "4820003333333")
        with self.assertRaises(ValueError):
            add_product(self.products, "Товар", 10.0, 2.5, "4820003333333")

    def test_find_product_by_barcode(self):
        found = find_product_by_barcode(self.products, "4820002222222")
        self.assertIsNotNone(found)
        self.assertEqual(found["name"], "Хліб")

        not_found = find_product_by_barcode(self.products, "9999999999999")
        self.assertIsNone(not_found)

if __name__ == "__main__":
    unittest.main()
