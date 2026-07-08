import unittest

from sales import add_to_cart, calculate_total, finish_sale, remove_from_cart


class TestSales(unittest.TestCase):
    def setUp(self):
        self.products = [
            {"name": "Молоко", "price": 32.50, "quantity": 10, "barcode": "4820001111111"},
            {"name": "Хліб", "price": 18.00, "quantity": 5, "barcode": "4820002222222"},
        ]
        self.cart = []
        self.sales_history = []

    def test_add_to_cart_and_total(self):
        add_to_cart(self.products, self.cart, "4820001111111")
        add_to_cart(self.products, self.cart, "4820001111111")

        self.assertEqual(self.cart[0]["quantity"], 2)
        self.assertEqual(calculate_total(self.cart), 65.0)
        self.assertEqual(calculate_total(self.cart, 10), 58.5)

    def test_remove_from_cart(self):
        add_to_cart(self.products, self.cart, "4820002222222")
        self.assertTrue(remove_from_cart(self.cart, "4820002222222"))
        self.assertEqual(self.cart, [])

    def test_finish_sale_updates_stock_and_history(self):
        add_to_cart(self.products, self.cart, "4820001111111")
        sale = finish_sale(self.products, self.cart, self.sales_history, 5)

        self.assertEqual(sale["total"], 30.88)
        self.assertEqual(self.products[0]["quantity"], 9)
        self.assertEqual(len(self.sales_history), 1)
        self.assertEqual(self.cart, [])


if __name__ == "__main__":
    unittest.main()
