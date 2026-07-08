import tkinter as tk
from tkinter import messagebox, ttk

from barcode_tools import create_barcode_image, generate_barcode_number
from products import add_product
from sales import add_to_cart, calculate_total, finish_sale, remove_from_cart
from storage import load_products, load_sales, save_products, save_sales


class MiniPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini POS System")
        self.root.geometry("900x620")

        self.products = load_products()
        self.sales_history = load_sales()
        self.cart = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_products_tab()
        self._build_cashier_tab()
        self._build_history_tab()

        self.refresh_products_table()
        self.refresh_cart_table()
        self.refresh_history_table()

    def _build_products_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Товари")

        form = ttk.LabelFrame(tab, text="Новий товар")
        form.pack(fill="x", padx=10, pady=10)

        self.product_name = tk.StringVar()
        self.product_price = tk.StringVar()
        self.product_quantity = tk.StringVar()
        self.product_barcode = tk.StringVar()

        labels = ["Назва товару", "Ціна", "Кількість", "Штрихкод"]
        variables = [self.product_name, self.product_price, self.product_quantity, self.product_barcode]

        for index, (label, variable) in enumerate(zip(labels, variables)):
            ttk.Label(form, text=label).grid(row=0, column=index, padx=5, pady=5, sticky="w")
            ttk.Entry(form, textvariable=variable, width=22).grid(row=1, column=index, padx=5, pady=5)

        ttk.Button(form, text="Generate barcode", command=self.generate_barcode).grid(row=1, column=4, padx=5)
        ttk.Button(form, text="Add product", command=self.add_product).grid(row=1, column=5, padx=5)
        ttk.Button(form, text="Save products", command=self.save_products).grid(row=2, column=4, padx=5, pady=5)
        ttk.Button(form, text="Load products", command=self.load_products).grid(row=2, column=5, padx=5, pady=5)

        self.products_table = ttk.Treeview(
            tab,
            columns=("name", "price", "quantity", "barcode"),
            show="headings",
            height=16,
        )
        for column, title in [
            ("name", "Назва"),
            ("price", "Ціна"),
            ("quantity", "Кількість"),
            ("barcode", "Штрихкод"),
        ]:
            self.products_table.heading(column, text=title)
            self.products_table.column(column, width=160)
        self.products_table.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_cashier_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Каса")

        top = ttk.Frame(tab)
        top.pack(fill="x", padx=10, pady=10)

        self.cashier_barcode = tk.StringVar()
        self.discount_percent = tk.StringVar(value="0")

        ttk.Label(top, text="Введіть або відскануйте штрихкод").pack(side="left", padx=5)
        ttk.Entry(top, textvariable=self.cashier_barcode, width=30).pack(side="left", padx=5)
        ttk.Button(top, text="Add to receipt", command=self.add_to_receipt).pack(side="left", padx=5)
        ttk.Button(top, text="Remove item", command=self.remove_item).pack(side="left", padx=5)
        ttk.Button(top, text="Clear receipt", command=self.clear_receipt).pack(side="left", padx=5)
        ttk.Button(top, text="Finish sale", command=self.finish_sale).pack(side="left", padx=5)

        discount_frame = ttk.Frame(tab)
        discount_frame.pack(fill="x", padx=10)
        ttk.Label(discount_frame, text="Знижка %").pack(side="left", padx=5)
        ttk.Entry(discount_frame, textvariable=self.discount_percent, width=10).pack(side="left", padx=5)

        self.cart_table = ttk.Treeview(
            tab,
            columns=("name", "price", "quantity", "sum"),
            show="headings",
            height=16,
        )
        for column, title in [
            ("name", "Назва"),
            ("price", "Ціна"),
            ("quantity", "Кількість"),
            ("sum", "Сума"),
        ]:
            self.cart_table.heading(column, text=title)
            self.cart_table.column(column, width=180)
        self.cart_table.pack(fill="both", expand=True, padx=10, pady=10)

        self.total_label = ttk.Label(tab, text="Total: 0 грн", font=("Arial", 14, "bold"))
        self.total_label.pack(anchor="e", padx=20, pady=10)

    def _build_history_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Історія продажів")

        self.history_table = ttk.Treeview(
            tab,
            columns=("date", "total", "items_count"),
            show="headings",
            height=20,
        )
        for column, title in [
            ("date", "Дата"),
            ("total", "Сума продажу"),
            ("items_count", "Кількість товарів"),
        ]:
            self.history_table.heading(column, text=title)
            self.history_table.column(column, width=240)
        self.history_table.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_barcode(self):
        barcode = generate_barcode_number(product["barcode"] for product in self.products)
        self.product_barcode.set(barcode)
        create_barcode_image(barcode)
        messagebox.showinfo("Готово", f"Штрихкод створено: {barcode}")

    def add_product(self):
        try:
            product = add_product(
                self.products,
                self.product_name.get(),
                self.product_price.get(),
                self.product_quantity.get(),
                self.product_barcode.get(),
            )
            save_products(self.products)
            self.refresh_products_table()
            self.product_name.set("")
            self.product_price.set("")
            self.product_quantity.set("")
            self.product_barcode.set("")
            messagebox.showinfo("Готово", f"Товар додано: {product['name']}")
        except ValueError as exc:
            messagebox.showerror("Помилка", str(exc))

    def save_products(self):
        save_products(self.products)
        messagebox.showinfo("Готово", "Товари збережено")

    def load_products(self):
        self.products = load_products()
        self.refresh_products_table()
        messagebox.showinfo("Готово", "Товари завантажено")

    def add_to_receipt(self):
        try:
            add_to_cart(self.products, self.cart, self.cashier_barcode.get())
            self.cashier_barcode.set("")
            self.refresh_cart_table()
        except ValueError as exc:
            messagebox.showerror("Помилка", str(exc))

    def remove_item(self):
        selected = self.cart_table.selection()
        barcode = self.cart_table.item(selected[0])["tags"][0] if selected else self.cashier_barcode.get()
        remove_from_cart(self.cart, barcode)
        self.refresh_cart_table()

    def clear_receipt(self):
        self.cart.clear()
        self.refresh_cart_table()

    def finish_sale(self):
        try:
            discount = float(self.discount_percent.get() or 0)
            sale = finish_sale(self.products, self.cart, self.sales_history, discount)
            save_products(self.products)
            save_sales(self.sales_history)
            self.refresh_products_table()
            self.refresh_cart_table()
            self.refresh_history_table()
            messagebox.showinfo("Продаж завершено", f"Сума: {sale['total']} грн")
        except ValueError as exc:
            messagebox.showerror("Помилка", str(exc))

    def refresh_products_table(self):
        self.products_table.delete(*self.products_table.get_children())
        for product in self.products:
            self.products_table.insert(
                "",
                "end",
                values=(product["name"], product["price"], product["quantity"], product["barcode"]),
            )

    def refresh_cart_table(self):
        self.cart_table.delete(*self.cart_table.get_children())
        for item in self.cart:
            self.cart_table.insert(
                "",
                "end",
                values=(item["name"], item["price"], item["quantity"], item["sum"]),
                tags=(item["barcode"],),
            )
        try:
            discount = float(self.discount_percent.get() or 0)
        except ValueError:
            discount = 0
        self.total_label.config(text=f"Total: {calculate_total(self.cart, discount)} грн")

    def refresh_history_table(self):
        self.history_table.delete(*self.history_table.get_children())
        for sale in self.sales_history:
            self.history_table.insert("", "end", values=(sale["date"], sale["total"], sale["items_count"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPOSApp(root)
    root.mainloop()
