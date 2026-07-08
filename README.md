# Mini POS System (CASA)

POS (Point of Sale) — це касова програма для роботи з товарами та продажами.

## Можливості програми

Програма вміє:

- додавати товари;
- генерувати штрихкод для товару;
- шукати товар по штрихкоду;
- додавати товар у чек;
- рахувати суму;
- робити знижку;
- завершувати продаж;
- зберігати товари у файл;
- зберігати історію продажів.

---

## Фінальна ідея програми

### 1) Вкладка **“Товари”**

Тут адміністратор додає товар:

- Назва товару
- Ціна
- Кількість
- Штрихкод

Кнопки:

- `Generate barcode`
- `Add product`
- `Save products`
- `Load products`

Після натискання **Generate barcode** програма створює унікальний код, наприклад:

`4820001234567`

та генерує картинку штрихкоду.

---

### 2) Вкладка **“Каса”**

Тут касир продає товар:

- Введіть або відскануйте штрихкод

Кнопки:

- `Add to receipt`
- `Remove item`
- `Clear receipt`
- `Finish sale`

Таблиця чеку:

**Назва | Ціна | Кількість | Сума**

Знизу:

**Total: 1450 грн**

---

### 3) Вкладка **“Історія продажів”**

Тут відображається:

- Дата
- Сума продажу
- Кількість товарів

---

## Структура проєкту

```text
mini-pos-system/
│
├── main.py
├── products.py
├── barcode_tools.py
├── storage.py
├── sales.py
├── README.md
│
├── data/
│   ├── products.json
│   └── sales.json
│
└── barcodes/
    └── 4820001234567.png
```

---

## Розподіл задач у команді

### Кирил — інтерфейс каси  
**Гілка:** `feature/ui`

**Задачі:**

- головне вікно;
- вкладки через `ttk.Notebook`;
- вкладка “Товари”;
- вкладка “Каса”;
- вкладка “Історія”;
- таблиці через `ttk.Treeview`;
- кнопки;
- поля вводу.

**Коміти:**

```bash
git commit -m "Create main POS window"
git commit -m "Add products tab"
git commit -m "Add cashier tab"
git commit -m "Add sales history tab"
git commit -m "Add tables and buttons"
```

---

### Діма — логіка товарів і продажів  
**Гілка:** `feature/pos-logic`

**Задачі:**

- додавання товару;
- перевірка назви, ціни, кількості;
- пошук товару по штрихкоду;
- додавання товару в чек;
- підрахунок загальної суми;
- зменшення залишку товару після продажу;
- завершення продажу.

**Функції:**

- `add_product()`
- `find_product_by_barcode()`
- `add_to_cart()`
- `remove_from_cart()`
- `calculate_total()`
- `finish_sale()`

**Коміти:**

```bash
git commit -m "Add product validation"
git commit -m "Add product creation logic"
git commit -m "Add barcode product search"
git commit -m "Add cart logic"
git commit -m "Add sale finishing logic"
```

---

### Ярік — штрихкоди, файли, історія  
**Гілка:** `feature/barcodes-storage`

**Задачі:**

- генерація унікального штрихкоду;
- створення картинки штрихкоду;
- збереження товарів у `products.json`;
- збереження продажів у `sales.json`;
- створення папок `data/` і `barcodes/`;
- оформлення `README`.

**Функції:**

- `generate_barcode_number()`
- `create_barcode_image()`
- `save_products()`
- `load_products()`
- `save_sales()`
- `load_sales()`

**Коміти:**

```bash
git commit -m "Add barcode number generation"
git commit -m "Add barcode image generation"
git commit -m "Add JSON product storage"
git commit -m "Add sales history storage"
git commit -m "Add project README"
```

---

## Встановлення залежностей

Для `Tkinter` нічого додатково встановлювати не потрібно (у більшості Python-інсталяцій він уже є).

Для генерації штрихкодів встановіть:

```bash
pip install python-barcode pillow
```

---

## Як генерується штрихкод

Найпростіший варіант — **EAN-13**.

- EAN-13 має 13 цифр, наприклад: `4821234567890`
- Остання цифра — контрольна (checksum)
- Бібліотека може автоматично порахувати її, якщо передати перші 12 цифр

---

## Запуск проєкту

```bash
python main.py
```

> Переконайтеся, що папки `data/` та `barcodes/` існують, або створюйте їх автоматично під час запуску.
