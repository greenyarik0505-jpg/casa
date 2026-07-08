import tkinter as tk
from tkinter import ttk, messagebox

from storage import load_products, load_sales, save_products, save_sales
from barcode_tools import generate_barcode_number, create_barcode_image
import products as prod_logic
import sales


class MiniPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini POS System")
        self.root.geometry("900x550")

        self.products = load_products()
        self.sales_history = load_sales()

        # Налаштування стилів інтерфейсу
        self._setup_styles()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Будуємо вкладку Товари
        self._build_products_tab()

        # Будуємо вкладку Каса
        self._build_sales_tab()

        # Залишаємо Історію продажів як плейсхолдер
        self._add_placeholder_tab(
            "Історія продажів",
            "Історія продажів ще не підключена до інтерфейсу.",
        )

    def _setup_styles(self) -> None:
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Палітра кольорів
        bg_color = "#f9fafb"        # Світло-сірий фон
        card_color = "#ffffff"      # Білий для карток
        primary_color = "#4f46e5"   # Індиго
        primary_active = "#4338ca"  # Темніший індиго
        text_color = "#1f2937"      # Темно-сірий текст
        border_color = "#e5e7eb"    # Світла рамка
        danger_color = "#ef4444"    # Червоний
        danger_active = "#dc2626"

        self.root.configure(bg=bg_color)

        self.style.configure(".", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=bg_color, borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background="#f3f4f6",
            foreground="#4b5563",
            padding=[20, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", primary_color)],
            foreground=[("selected", "#ffffff")]
        )

        # Стилізація LabelFrame
        self.style.configure("TLabelframe", background=card_color, borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background=card_color, foreground=primary_color, font=("Segoe UI", 11, "bold"))

        self.style.configure("TFrame", background=bg_color)
        self.style.configure("Card.TFrame", background=card_color)

        self.style.configure("TLabel", background=card_color, foreground=text_color)
        self.style.configure("Form.TLabel", background=card_color, font=("Segoe UI", 10, "bold"))
        
        # Акцентна кнопка (Додати товар, Завершити продаж)
        self.style.configure(
            "Accent.TButton",
            background=primary_color,
            foreground="#ffffff",
            borderwidth=0,
            focuscolor=primary_color,
            padding=[12, 8],
            font=("Segoe UI", 10, "bold")
        )
        self.style.map("Accent.TButton", background=[("active", primary_active)])

        # Другорядна кнопка (Генерувати, Зберегти, Завантажити, Очистити кошик)
        self.style.configure(
            "Secondary.TButton",
            background="#e5e7eb",
            foreground="#374151",
            borderwidth=0,
            padding=[10, 6],
            font=("Segoe UI", 9, "bold")
        )
        self.style.map("Secondary.TButton", background=[("active", "#d1d5db")])

        # Кнопка небезпеки (Видалити)
        self.style.configure(
            "Danger.TButton",
            background=danger_color,
            foreground="#ffffff",
            borderwidth=0,
            padding=[10, 6],
            font=("Segoe UI", 9, "bold")
        )
        self.style.map("Danger.TButton", background=[("active", danger_active)])

        # Стилізація таблиці (Treeview)
        self.style.configure(
            "Treeview",
            background=card_color,
            fieldbackground=card_color,
            foreground=text_color,
            rowheight=28,
            borderwidth=0
        )
        self.style.configure(
            "Treeview.Heading",
            background="#f3f4f6",
            foreground="#374151",
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="flat"
        )
        self.style.map("Treeview", background=[("selected", "#e0e7ff")], foreground=[("selected", primary_color)])

    def _build_products_tab(self) -> None:
        # Головний фрейм вкладки
        self.products_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.products_tab, text="Товари")

        # Ліва панель: Форма додавання товару
        self.left_panel = ttk.LabelFrame(self.products_tab, text=" Додати новий товар ", padding=15)
        self.left_panel.pack(side="left", fill="both", expand=False, padx=(15, 8), pady=15)

        # Поля форми
        ttk.Label(self.left_panel, text="Назва товару:", style="Form.TLabel").pack(anchor="w", pady=(0, 4))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.left_panel, textvariable=self.name_var, font=("Segoe UI", 10), width=28)
        self.name_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(self.left_panel, text="Ціна (грн):", style="Form.TLabel").pack(anchor="w", pady=(0, 4))
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(self.left_panel, textvariable=self.price_var, font=("Segoe UI", 10), width=28)
        self.price_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(self.left_panel, text="Кількість (шт):", style="Form.TLabel").pack(anchor="w", pady=(0, 4))
        self.qty_var = tk.StringVar()
        self.qty_entry = ttk.Entry(self.left_panel, textvariable=self.qty_var, font=("Segoe UI", 10), width=28)
        self.qty_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(self.left_panel, text="Штрихкод (EAN-13):", style="Form.TLabel").pack(anchor="w", pady=(0, 4))
        
        # Рамка для поля штрихкоду та кнопки генерації поруч
        barcode_frame = ttk.Frame(self.left_panel, style="Card.TFrame")
        barcode_frame.pack(fill="x", pady=(0, 15))
        
        self.barcode_var = tk.StringVar()
        self.barcode_entry = ttk.Entry(barcode_frame, textvariable=self.barcode_var, font=("Segoe UI", 10), width=16)
        self.barcode_entry.pack(side="left", fill="x", expand=True)
        
        btn_gen = ttk.Button(barcode_frame, text="Генерувати", command=self._generate_barcode, style="Secondary.TButton")
        btn_gen.pack(side="right", padx=(8, 0))

        # Кнопка додавання товару
        btn_add = ttk.Button(self.left_panel, text="Додати товар", command=self._add_product, style="Accent.TButton")
        btn_add.pack(fill="x", pady=(5, 10))

        # Розділювач
        separator = ttk.Separator(self.left_panel, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Збереження/Завантаження
        btn_save = ttk.Button(self.left_panel, text="Зберегти товари", command=self._save_products, style="Secondary.TButton")
        btn_save.pack(fill="x", pady=(0, 6))

        btn_load = ttk.Button(self.left_panel, text="Завантажити товари", command=self._load_products, style="Secondary.TButton")
        btn_load.pack(fill="x")

        # Права панель: Таблиця наявних товарів
        self.right_panel = ttk.LabelFrame(self.products_tab, text=" Список товарів ", padding=15)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(8, 15), pady=15)

        # Контейнер для таблиці та прокрутки
        table_container = ttk.Frame(self.right_panel, style="Card.TFrame")
        table_container.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("barcode", "name", "price", "quantity")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=10)
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("barcode", text="Штрихкод")
        self.tree.heading("name", text="Назва")
        self.tree.heading("price", text="Ціна (грн)")
        self.tree.heading("quantity", text="Кількість")

        self.tree.column("barcode", width=140, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("price", width=90, anchor="e")
        self.tree.column("quantity", width=90, anchor="e")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Панель дій для таблиці (видалення товару)
        actions_container = ttk.Frame(self.right_panel, style="Card.TFrame")
        actions_container.pack(fill="x")

        btn_delete = ttk.Button(actions_container, text="Видалити вибраний товар", command=self._delete_product, style="Danger.TButton")
        btn_delete.pack(side="left")

        # Відображення наявних товарів
        self._refresh_tree()

    def _build_sales_tab(self) -> None:
        self.cart = []  # Кошик покупця
        
        # Головний фрейм вкладки Каса
        self.sales_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.sales_tab, text="Каса")
        
        # Верхня панель сканування
        scan_frame = ttk.LabelFrame(self.sales_tab, text=" Сканування / Введення штрихкоду ", padding=12)
        scan_frame.pack(side="top", fill="x", padx=15, pady=(15, 5))
        
        ttk.Label(scan_frame, text="Штрихкод товару:", style="Form.TLabel").pack(side="left", padx=(5, 5))
        
        self.sales_barcode_var = tk.StringVar()
        self.sales_barcode_entry = ttk.Entry(scan_frame, textvariable=self.sales_barcode_var, font=("Segoe UI", 10), width=35)
        self.sales_barcode_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.sales_barcode_entry.bind("<Return>", lambda event: self._add_to_cart())
        
        btn_add_cart = ttk.Button(scan_frame, text="Додати в чек", command=self._add_to_cart, style="Accent.TButton")
        btn_add_cart.pack(side="right", padx=5)
        
        # Центральна панель: Чек (Таблиця кошика)
        cart_frame = ttk.LabelFrame(self.sales_tab, text=" Чек ", padding=12)
        cart_frame.pack(side="top", fill="both", expand=True, padx=15, pady=5)
        
        table_container = ttk.Frame(cart_frame, style="Card.TFrame")
        table_container.pack(fill="both", expand=True, pady=(0, 5))
        
        columns = ("barcode", "name", "price", "quantity", "subtotal")
        self.cart_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=8)
        self.cart_tree.pack(side="left", fill="both", expand=True)
        
        self.cart_tree.heading("barcode", text="Штрихкод")
        self.cart_tree.heading("name", text="Назва товару")
        self.cart_tree.heading("price", text="Ціна (грн)")
        self.cart_tree.heading("quantity", text="Кількість")
        self.cart_tree.heading("subtotal", text="Сума (грн)")
        
        self.cart_tree.column("barcode", width=140, anchor="center")
        self.cart_tree.column("name", width=280, anchor="w")
        self.cart_tree.column("price", width=95, anchor="e")
        self.cart_tree.column("quantity", width=90, anchor="center")
        self.cart_tree.column("subtotal", width=95, anchor="e")
        
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.cart_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        
        # Нижня панель: Знижки, Разом та Кнопки дій
        bottom_frame = ttk.Frame(self.sales_tab, style="Card.TFrame")
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=(5, 15))
        
        # Ліва частина нижньої панелі (Дії з чеком)
        left_actions = ttk.Frame(bottom_frame, style="Card.TFrame")
        left_actions.pack(side="left", fill="y", pady=5)
        
        btn_remove_item = ttk.Button(left_actions, text="Видалити позицію", command=self._remove_from_cart, style="Danger.TButton")
        btn_remove_item.pack(side="left", padx=5)
        
        btn_clear_cart = ttk.Button(left_actions, text="Очистити чек", command=self._clear_cart, style="Secondary.TButton")
        btn_clear_cart.pack(side="left", padx=5)
        
        # Права частина нижньої панелі (Знижки, Суми, Завершення)
        right_info = ttk.Frame(bottom_frame, style="Card.TFrame")
        right_info.pack(side="right", fill="y", pady=5)
        
        # Знижка
        discount_frame = ttk.Frame(right_info, style="Card.TFrame")
        discount_frame.pack(side="top", anchor="e", pady=2)
        
        ttk.Label(discount_frame, text="Знижка (%):", style="Form.TLabel").pack(side="left", padx=5)
        self.discount_var = tk.StringVar(value="0")
        self.discount_entry = ttk.Entry(discount_frame, textvariable=self.discount_var, width=6, font=("Segoe UI", 10, "bold"), justify="center")
        self.discount_entry.pack(side="left", padx=5)
        self.discount_var.trace_add("write", lambda *args: self._recalculate_totals())
        
        # Інформаційні мітки сум
        self.lbl_subtotal = ttk.Label(right_info, text="Сума: 0.00 грн", font=("Segoe UI", 10))
        self.lbl_subtotal.pack(side="top", anchor="e", pady=1)
        
        self.lbl_discount = ttk.Label(right_info, text="Знижка: 0.00 грн", font=("Segoe UI", 10))
        self.lbl_discount.pack(side="top", anchor="e", pady=1)
        
        self.lbl_total = ttk.Label(right_info, text="Разом: 0.00 грн", font=("Segoe UI", 13, "bold"), foreground="#4f46e5")
        self.lbl_total.pack(side="top", anchor="e", pady=3)
        
        # Кнопка Оформити продаж
        btn_checkout = ttk.Button(right_info, text="Завершити продаж", command=self._finish_sale, style="Accent.TButton")
        btn_checkout.pack(side="top", anchor="e", pady=(8, 0))

    def _generate_barcode(self) -> None:
        existing = [p["barcode"] for p in self.products]
        try:
            barcode = generate_barcode_number(existing)
            self.barcode_var.set(barcode)
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося згенерувати штрихкод: {e}")

    def _add_product(self) -> None:
        name = self.name_var.get()
        price = self.price_var.get()
        qty = self.qty_var.get()
        barcode = self.barcode_var.get()

        try:
            # Виклик бізнес-логіки додавання товару
            self.products = prod_logic.add_product(self.products, name, price, qty, barcode)
            
            # Генерація зображення штрихкоду
            create_barcode_image(barcode)
            
            # Автоматичне збереження
            save_products(self.products)
            
            # Оновлення таблиці
            self._refresh_tree()
            
            # Очищення полів форми
            self.name_var.set("")
            self.price_var.set("")
            self.qty_var.set("")
            self.barcode_var.set("")
            
            messagebox.showinfo("Успіх", f"Товар '{name}' успішно додано!")
        except ValueError as e:
            messagebox.showerror("Помилка валідації", str(e))
        except Exception as e:
            messagebox.showerror("Помилка", f"Невідома помилка при додаванні: {e}")

    def _delete_product(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Попередження", "Будь ласка, виберіть товар для видалення зі списку.")
            return

        item_values = self.tree.item(selected_item, "values")
        barcode = item_values[0]
        name = item_values[1]

        confirm = messagebox.askyesno(
            "Підтвердження видалення",
            f"Ви дійсно хочете видалити товар '{name}' (Штрихкод: {barcode})?"
        )
        if confirm:
            self.products = [p for p in self.products if p["barcode"] != barcode]
            save_products(self.products)
            self._refresh_tree()
            messagebox.showinfo("Успіх", f"Товар '{name}' успішно видалено.")

    def _save_products(self) -> None:
        try:
            save_products(self.products)
            messagebox.showinfo("Збереження", "Товари успішно збережено у файл!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти товари: {e}")

    def _load_products(self) -> None:
        try:
            self.products = load_products()
            self._refresh_tree()
            messagebox.showinfo("Завантаження", "Товари успішно завантажено з файлу!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити товари: {e}")

    def _refresh_tree(self) -> None:
        # Очищуємо таблицю
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Заповнюємо даними
        for p in self.products:
            self.tree.insert(
                "",
                "end",
                values=(p["barcode"], p["name"], f"{float(p['price']):.2f}", p["quantity"])
            )

    # Дії з кошиком
    def _add_to_cart(self) -> None:
        barcode = self.sales_barcode_var.get().strip()
        if not barcode:
            return
            
        # Шукаємо товар за штрихкодом
        product = prod_logic.find_product_by_barcode(self.products, barcode)
        if not product:
            messagebox.showwarning("Попередження", f"Товар зі штрихкодом '{barcode}' не знайдено в базі!")
            return
            
        try:
            self.cart = sales.add_to_cart(self.cart, product, 1)
            self._refresh_cart_tree()
            self._recalculate_totals()
            self.sales_barcode_var.set("")  # Очищуємо поле
        except ValueError as e:
            messagebox.showerror("Помилка додавання", str(e))

    def _remove_from_cart(self) -> None:
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showwarning("Попередження", "Будь ласка, виберіть товар для видалення з чека.")
            return
            
        item_values = self.cart_tree.item(selected_item, "values")
        barcode = item_values[0]
        
        self.cart = sales.remove_from_cart(self.cart, barcode)
        self._refresh_cart_tree()
        self._recalculate_totals()

    def _clear_cart(self) -> None:
        if not self.cart:
            return
        confirm = messagebox.askyesno("Очистити чек", "Ви впевнені, що хочете очистити весь чек?")
        if confirm:
            self.cart = []
            self._refresh_cart_tree()
            self._recalculate_totals()

    def _recalculate_totals(self) -> None:
        discount_str = self.discount_var.get().strip()
        try:
            discount = float(discount_str) if discount_str else 0.0
        except ValueError:
            discount = 0.0

        try:
            subtotal, disc_amt, total = sales.calculate_total(self.cart, discount)
            self.lbl_subtotal.configure(text=f"Сума: {subtotal:.2f} грн")
            self.lbl_discount.configure(text=f"Знижка: {disc_amt:.2f} грн")
            self.lbl_total.configure(text=f"Разом: {total:.2f} грн")
        except ValueError:
            self.lbl_subtotal.configure(text="Сума: 0.00 грн")
            self.lbl_discount.configure(text="Знижка: 0.00 грн")
            self.lbl_total.configure(text="Разом: 0.00 грн")

    def _finish_sale(self) -> None:
        if not self.cart:
            messagebox.showwarning("Попередження", "Кошик порожній, неможливо завершити продаж.")
            return

        discount_str = self.discount_var.get().strip()
        try:
            discount = float(discount_str) if discount_str else 0.0
            if not (0.0 <= discount <= 100.0):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Помилка", "Знижка повинна бути числом від 0 до 100.")
            return

        try:
            # Оформлення продажу на бекенді
            self.products, self.sales_history, sale_record = sales.finish_sale(
                self.products, self.cart, self.sales_history, discount
            )
            
            # Збереження оновлених файлів
            save_products(self.products)
            save_sales(self.sales_history)
            
            # Очищення кошика та інтерфейсу
            self.cart = []
            self._refresh_cart_tree()
            self.discount_var.set("0")
            self._recalculate_totals()
            
            # Синхронізація таблиці вкладки Товари
            self._refresh_tree()
            
            messagebox.showinfo(
                "Успіх",
                f"Продаж №{sale_record['id']} успішно проведено!\n"
                f"Разом до сплати: {sale_record['total']:.2f} грн"
            )
        except ValueError as e:
            messagebox.showerror("Помилка завершення продажу", str(e))
        except Exception as e:
            messagebox.showerror("Помилка", f"Невідома помилка: {e}")

    def _refresh_cart_tree(self) -> None:
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        for item in self.cart:
            self.cart_tree.insert(
                "",
                "end",
                values=(item["barcode"], item["name"], f"{item['price']:.2f}", item["quantity"], f"{item['subtotal']:.2f}")
            )

    def _add_placeholder_tab(self, title: str, text: str) -> None:
        tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(tab, text=title)
        ttk.Label(tab, text=text, font=("Arial", 12), justify="center").pack(expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    MiniPOSApp(root)
    root.mainloop()
