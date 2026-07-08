# CASA — Mini POS System

Легкий навчальний POS (Point of Sale) застосунок для роботи з товарами, чеками та історією продажів.

## ✨ Основні можливості

- Додавання товарів (назва, ціна, кількість, штрихкод)
- Генерація унікальних EAN-13 штрихкодів та зображень
- Пошук товару за штрихкодом
- Формування чека (додавання/видалення позицій, очищення, завершення продажу)
- Підрахунок суми та застосування знижки
- Збереження/завантаження товарів і продажів у JSON

## 🚀 Quick Start

### 1) Встановіть залежності

```bash
pip install python-barcode pillow
```

> `tkinter` зазвичай вже входить до стандартної інсталяції Python.

### 2) Запустіть застосунок

```bash
python main.py
```

### 3) Переконайтесь, що існують папки даних

- `data/` — для `products.json` та `sales.json`
- `barcodes/` — для PNG-файлів штрихкодів

## 🧩 Структура проєкту

```text
mini-pos-system/
├── main.py
├── products.py
├── barcode_tools.py
├── storage.py
├── sales.py
├── data/
│   ├── products.json
│   └── sales.json
├── barcodes/
│   └── 4820001234567.png
└── README.md
```

## 🖥️ Основні екрани

### Товари

- Додавання нових товарів
- Генерація штрихкоду (`Generate barcode`)
- Збереження/завантаження (`Save products` / `Load products`)

### Каса

- Сканування або введення штрихкоду
- Формування чека (`Add to receipt`, `Remove item`, `Clear receipt`)
- Завершення продажу (`Finish sale`)

### Історія продажів

- Перегляд дати, суми продажу та кількості товарів по операції

## 📊 GitHub Graphs

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=greenyarik0505-jpg&show_icons=true&theme=transparent)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=greenyarik0505-jpg&layout=compact&theme=transparent)

[![Contribution Graph](https://github-readme-activity-graph.vercel.app/graph?username=greenyarik0505-jpg&theme=github-compact)](https://github.com/greenyarik0505-jpg)

## 🗺️ Roadmap

- [ ] Додати редагування товарів прямо з таблиці
- [ ] Додати експорт чеків у CSV/PDF
- [ ] Додати базову аналітику продажів по датах
