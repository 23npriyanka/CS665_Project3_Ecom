# E-Commerce Manager — CS665 Project 3

A full-stack Flask web application for managing an e-commerce database with Customers, Sellers, Products, and Orders.

---

## Project Description

This app is a CRUD-based management portal built on the e-commerce schema from Project 2. It allows staff/admins to:
- Manage customers, sellers, products, and orders
- View all orders placed by a specific customer (One-to-Many relationship)
- Create orders as atomic SQL transactions (Order + OrderItems together)
- See a live dashboard with aggregate stats (COUNT, SUM, AVG)
- Enforce server-side validation on all inputs

---

## Tech Stack

| Layer     | Technology                         |
|-----------|------------------------------------|
| Language  | Python 3                           |
| Framework | Flask                              |
| Database  | SQLite (via SQLAlchemy ORM)        |
| Frontend  | HTML5, Bootstrap 5.3, Jinja2       |
| VCS       | Git                                |

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ecommerce_app
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Database Setup

### Option A — Seed with sample data (recommended for first run)
```bash
python seed.py
```
This creates `ecommerce.db` in the project folder and inserts the original 5 customers, 5 sellers, 5 products, and 5 orders from the DDL.

### Option B — Empty database
```bash
python -c "from app import app; from database import db; app.app_context().push(); db.create_all()"
```

---

## Usage Details

### Start the development server
```bash
python app.py
```

Then open your browser and navigate to: **http://127.0.0.1:5000**

### Main Features

| Route                    | Feature                                       |
|--------------------------|-----------------------------------------------|
| `/`                      | Dashboard with aggregate stats                |
| `/customers`             | List, add, edit, delete customers             |
| `/customers/<id>/orders` | View all orders for a customer (1-to-Many)    |
| `/sellers`               | List, add, edit, delete sellers               |
| `/products`              | List, add, edit, delete products              |
| `/orders`                | List, add, edit, delete orders                |
| `/orders/add`            | Place new order using a SQL transaction       |

---

## Requirements File

```
Flask>=3.0
Flask-SQLAlchemy>=3.1
```

Generate with:
```bash
pip freeze > requirements.txt
```

---

## .gitignore

```
venv/
__pycache__/
*.pyc
*.db
.env
instance/
```

---

## Project Structure

```
ecommerce_app/
├── app.py              # Flask routes & application logic
├── database.py         # SQLAlchemy models
├── seed.py             # Database seeder
├── requirements.txt
├── README.md
├── NORMALIZATION.md
├── AI_LOG.md
├── schema.sql
├── static/
│   └── css/style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── customers.html
    ├── customer_form.html
    ├── customer_orders.html
    ├── sellers.html
    ├── seller_form.html
    ├── products.html
    ├── product_form.html
    ├── orders.html
    ├── order_form.html
    └── order_edit.html
```
