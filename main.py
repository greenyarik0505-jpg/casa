import tkinter as tk
from tkinter import ttk

from storage import load_products, load_sales


class MiniPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini POS System")
        self.root.geometry("700x420")

        self.products = load_products()
        self.sales_history = load_sales()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._add_placeholder_tab(
            "Товари",
            "Вкладка товарів ще не дороблена.\nГотові тільки файли storage.py і barcode_tools.py.",
        )
        self._add_placeholder_tab(
            "Каса",
            "Каса ще не працює.\nДодавання в чек, знижки і завершення продажу не реалізовані.",
        )
        self._add_placeholder_tab(
            "Історія продажів",
            "Історія продажів ще не підключена до інтерфейсу.",
        )

    def _add_placeholder_tab(self, title: str, text: str) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        ttk.Label(tab, text=text, font=("Arial", 12), justify="center").pack(expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    MiniPOSApp(root)
    root.mainloop()
