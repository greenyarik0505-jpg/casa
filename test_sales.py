import unittest
from sales import add_to_cart, remove_from_cart, calculate_total, finish_sale

class TestSales(unittest.TestCase):
    def setUp(self):
        self.products = [
            {"name": "Молоко", "price": 32.50, "quantity": 10, "barcode": "4820001111111"},
            {"name": "Хліб", "price": 18.00, "quantity": 5, "barcode": "4820002222222"}
        ]
        self.cart = []
        self.sales_history = []

    def test_add_to_cart_success(self):
        # Додавання товару, якого ще немає в кошику
        self.cart = add_to_cart(self.cart, self.products[0], 2)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]["barcode"], "4820001111111")
        self.assertEqual(self.cart[0]["quantity"], 2)
        self.assertEqual(self.cart[0]["subtotal"], 65.00)

        # Збільшення кількості того ж товару
        self.cart = add_to_cart(self.cart, self.products[0], 3)
        self.assertEqual(self.cart[0]["quantity"], 5)
        self.assertEqual(self.cart[0]["subtotal"], 162.50)

    def test_add_to_cart_insufficient_stock(self):
        # На складі лише 10 одиниць Молока
        with self.assertRaises(ValueError) as context:
            add_to_cart(self.cart, self.products[0], 11)
        self.assertIn("Недостатньо товару", str(context.exception))

    def test_remove_from_cart(self):
        self.cart = add_to_cart(self.cart, self.products[0], 2)
        self.cart = add_to_cart(self.cart, self.products[1], 1)
        self.assertEqual(len(self.cart), 2)

        self.cart = remove_from_cart(self.cart, "4820001111111")
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]["barcode"], "4820002222222")

    def test_calculate_total_no_discount(self):
        self.cart = add_to_cart(self.cart, self.products[0], 2) # 65.00
        self.cart = add_to_cart(self.cart, self.products[1], 1) # 18.00
        subtotal, discount_amount, total = calculate_total(self.cart)
        self.assertEqual(subtotal, 83.00)
        self.assertEqual(discount_amount, 0.00)
        self.assertEqual(total, 83.00)

    def test_calculate_total_with_discount(self):
        self.cart = add_to_cart(self.cart, self.products[0], 2) # 65.00
        self.cart = add_to_cart(self.cart, self.products[1], 1) # 18.00
        subtotal, discount_amount, total = calculate_total(self.cart, 10.0) # 10%
        self.assertEqual(subtotal, 83.00)
        self.assertEqual(discount_amount, 8.30)
        self.assertEqual(total, 74.70)

    def test_finish_sale_success(self):
        self.cart = add_to_cart(self.cart, self.products[0], 2) # 10 -> 8
        self.cart = add_to_cart(self.cart, self.products[1], 3) # 5 -> 2
        
        updated_products, updated_history, sale_record = finish_sale(
            self.products, self.cart, self.sales_history, 10.0
        )

        # Перевірка оновлення залишків
        self.assertEqual(updated_products[0]["quantity"], 8)
        self.assertEqual(updated_products[1]["quantity"], 2)

        # Перевірка створення чека в історії
        self.assertEqual(len(updated_history), 1)
        self.assertEqual(sale_record["id"], 1)
        self.assertEqual(sale_record["total"], 107.10) # (65.00 + 54.00) - 10% = 119.00 - 11.90 = 107.10

if __name__ == "__main__":
    unittest.main()
