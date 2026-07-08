import tkinter as tk
from tkinter import messagebox, ttk

from barcode_tools import create_barcode_image, generate_barcode_number
import products as product_logic
from sales import add_to_cart, calculate_total, finish_sale, remove_from_cart
from storage import load_products, load_sales, save_products, save_sales


class MiniPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini POS System")
        self.root.geometry("1000x640")
        self.root.minsize(900, 560)

        self.products = load_products()
        self.sales_history = load_sales()
        self.cart = []

        self._setup_styles()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self._build_products_tab()
        self._build_cashier_tab()
        self._build_history_tab()

        self._refresh_products_table()
        self._refresh_cart_table()
        self._refresh_history_table()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        self.root.configure(bg="#f6f7fb")

        style.configure(".", font=("Segoe UI", 10))
        style.configure("TNotebook", background="#f6f7fb", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 8), font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe", background="#ffffff", borderwidth=1)
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        style.configure("TFrame", background="#f6f7fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff")
        style.configure("Form.TLabel", background="#ffffff", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=28, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_products_tab(self) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Товари")

        form = ttk.LabelFrame(tab, text="Додати товар", padding=12)
        form.pack(side="left", fill="y", padx=(10, 6), pady=10)

        self.name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.barcode_var = tk.StringVar()

        self._add_labeled_entry(form, "Назва товару", self.name_var)
        self._add_labeled_entry(form, "Ціна", self.price_var)
        self._add_labeled_entry(form, "Кількість", self.qty_var)
        self._add_labeled_entry(form, "Штрихкод", self.barcode_var)

        ttk.Button(form, text="Generate barcode", command=self._generate_barcode).pack(fill="x", pady=(8, 4))
        ttk.Button(form, text="Add product", command=self._add_product).pack(fill="x", pady=4)
        ttk.Button(form, text="Save products", command=self._save_products).pack(fill="x", pady=4)
        ttk.Button(form, text="Load products", command=self._load_products).pack(fill="x", pady=4)

        table_frame = ttk.LabelFrame(tab, text="Список товарів", padding=12)
        table_frame.pack(side="right", fill="both", expand=True, padx=(6, 10), pady=10)

        self.products_table = self._create_treeview(
            table_frame,
            ("barcode", "name", "price", "quantity"),
            {
                "barcode": "Штрихкод",
                "name": "Назва",
                "price": "Ціна",
                "quantity": "Кількість",
            },
        )

    def _build_cashier_tab(self) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Каса")

        controls = ttk.LabelFrame(tab, text="Продаж", padding=12)
        controls.pack(fill="x", padx=10, pady=10)

        self.cashier_barcode_var = tk.StringVar()
        self.discount_var = tk.StringVar(value="0")

        ttk.Label(controls, text="Введіть або відскануйте штрихкод").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Entry(controls, textvariable=self.cashier_barcode_var, width=28).grid(row=1, column=0, padx=4, pady=4)
        ttk.Button(controls, text="Add to receipt", command=self._add_to_receipt).grid(row=1, column=1, padx=4)
        ttk.Button(controls, text="Remove item", command=self._remove_receipt_item).grid(row=1, column=2, padx=4)
        ttk.Button(controls, text="Clear receipt", command=self._clear_receipt).grid(row=1, column=3, padx=4)
        ttk.Button(controls, text="Finish sale", command=self._finish_sale).grid(row=1, column=4, padx=4)

        ttk.Label(controls, text="Знижка %").grid(row=0, column=5, sticky="w", padx=(18, 4))
        ttk.Entry(controls, textvariable=self.discount_var, width=10).grid(row=1, column=5, padx=(18, 4), pady=4)
        ttk.Button(controls, text="Apply", command=self._refresh_cart_table).grid(row=1, column=6, padx=4)

        table_frame = ttk.LabelFrame(tab, text="Чек", padding=12)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.cart_table = self._create_treeview(
            table_frame,
            ("barcode", "name", "price", "quantity", "sum"),
            {
                "barcode": "Штрихкод",
                "name": "Назва",
                "price": "Ціна",
                "quantity": "Кількість",
                "sum": "Сума",
            },
        )

        self.total_label = ttk.Label(tab, text="Total: 0.00 грн", font=("Segoe UI", 14, "bold"))
        self.total_label.pack(anchor="e", padx=20, pady=(0, 12))

    def _build_history_tab(self) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Історія продажів")

        table_frame = ttk.LabelFrame(tab, text="Історія продажів", padding=12)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.history_table = self._create_treeview(
            table_frame,
            ("date", "total", "items_count", "discount_percent"),
            {
                "date": "Дата",
                "total": "Сума продажу",
                "items_count": "Кількість товарів",
                "discount_percent": "Знижка %",
            },
        )
        ttk.Button(tab, text="Reload history", command=self._load_sales_history).pack(anchor="e", padx=20, pady=(0, 12))

    def _add_labeled_entry(self, parent, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=label, style="Form.TLabel").pack(anchor="w", pady=(6, 2))
        ttk.Entry(parent, textvariable=variable, width=28).pack(fill="x")

    def _create_treeview(self, parent, columns: tuple[str, ...], headings: dict[str, str]) -> ttk.Treeview:
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(container, columns=columns, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(column, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        return tree

    def _generate_barcode(self) -> None:
        existing = [product.get("barcode", "") for product in self.products]
        barcode = generate_barcode_number(existing)
        self.barcode_var.set(barcode)
        create_barcode_image(barcode)

    def _add_product(self) -> None:
        barcode = self.barcode_var.get()
        if not barcode:
            self._generate_barcode()
            barcode = self.barcode_var.get()

        try:
            self.products = product_logic.add_product(
                self.products,
                self.name_var.get(),
                self.price_var.get(),
                self.qty_var.get(),
                barcode,
            )
            create_barcode_image(barcode)
            save_products(self.products)
            self._clear_product_form()
            self._refresh_products_table()
            messagebox.showinfo("Готово", "Товар додано")
        except ValueError as exc:
            messagebox.showerror("Помилка", str(exc))

    def _delete_selected_product(self) -> None:
        selected = self.products_table.selection()
        if not selected:
            return
        barcode = self.products_table.item(selected[0], "values")[0]
        self.products = [product for product in self.products if product["barcode"] != barcode]
        save_products(self.products)
        self._refresh_products_table()

    def _save_products(self) -> None:
        save_products(self.products)
        messagebox.showinfo("Готово", "Товари збережено")

    def _load_products(self) -> None:
        self.products = load_products()
        self._refresh_products_table()
        messagebox.showinfo("Готово", "Товари завантажено")

    def _add_to_receipt(self) -> None:
        try:
            add_to_cart(self.products, self.cart, self.cashier_barcode_var.get())
            self.cashier_barcode_var.set("")
            self._refresh_cart_table()
        except ValueError as exc:
            messagebox.showerror("Помилка", str(exc))

    def _remove_receipt_item(self) -> None:
        barcode = self.cashier_barcode_var.get().strip()
        selected = self.cart_table.selection()
        if selected:
            barcode = self.cart_table.item(selected[0], "values")[0]
        if not barcode:
            messagebox.showwarning("Увага", "Виберіть товар у чеку або введіть штрихкод")
            return
        remove_from_cart(self.cart, barcode)
        self._refresh_cart_table()

    def _clear_receipt(self) -> None:
        self.cart.clear()
        self._refresh_cart_table()

    def _finish_sale(self) -> None:
        try:
            sale = finish_sale(self.products, self.cart, self.sales_history, self.discount_var.get())
            save_products(self.products)
            save_sales(self.sales_history)
            self._refresh_products_table()
            self._refresh_cart_table()
            self._refresh_history_table()
            messagebox.showinfo("Продаж завершено", f"Сума: {sale['total']:.2f} грн")
        except ValueError as exc:
            messagebox.showerror("Помилка", str(exc))

    def _load_sales_history(self) -> None:
        self.sales_history = load_sales()
        self._refresh_history_table()

    def _clear_product_form(self) -> None:
        self.name_var.set("")
        self.price_var.set("")
        self.qty_var.set("")
        self.barcode_var.set("")

    def _refresh_products_table(self) -> None:
        self.products_table.delete(*self.products_table.get_children())
        for product in self.products:
            self.products_table.insert(
                "",
                "end",
                values=(
                    product.get("barcode", ""),
                    product.get("name", ""),
                    f"{float(product.get('price', 0)):.2f}",
                    product.get("quantity", 0),
                ),
            )

    def _refresh_cart_table(self) -> None:
        self.cart_table.delete(*self.cart_table.get_children())
        for item in self.cart:
            self.cart_table.insert(
                "",
                "end",
                values=(
                    item["barcode"],
                    item["name"],
                    f"{item['price']:.2f}",
                    item["quantity"],
                    f"{item['sum']:.2f}",
                ),
            )

        try:
            total = calculate_total(self.cart, self.discount_var.get())
        except ValueError:
            total = sum(float(item.get("sum", 0)) for item in self.cart)
        self.total_label.config(text=f"Total: {total:.2f} грн")

    def _refresh_history_table(self) -> None:
        self.history_table.delete(*self.history_table.get_children())
        for sale in self.sales_history:
            self.history_table.insert(
                "",
                "end",
                values=(
                    sale.get("date", ""),
                    f"{float(sale.get('total', 0)):.2f}",
                    sale.get("items_count", 0),
                    sale.get("discount_percent", 0),
                ),
            )


if __name__ == "__main__":
    root = tk.Tk()
    MiniPOSApp(root)
    root.mainloop()
