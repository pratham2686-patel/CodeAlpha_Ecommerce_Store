# ElectroMart - Django E-Commerce Store

ElectroMart is a full-stack e-commerce web application built using Python, Django, and JavaScript. I developed this project as part of the CodeAlpha Web Development Internship.

The goal of this project was to build a clean and responsive online shopping experience with features like instant cart updates, real-time order tracking, and invoice generation.

---

## Features

### Product Catalog and Browsing
- Browse products across different tech categories (Audio, Laptops, Gadgets, etc.).
- Search products by keyword or category name.
- Filter products by minimum/maximum price, star ratings, and in-stock availability.
- Sort products by newest, price (low to high / high to low), and ratings.
- Pagination that remembers your current search and filter choices.
- Horizontal carousel showing recently viewed items based on session history.

### Cart and Checkout (No Page Reload)
- Add items to the cart directly from the home or product page using AJAX.
- Update quantities or delete products directly on the cart page without refreshing.
- Save items from cart to wishlist with a single click.
- Real-time client-side form validation during checkout (flags invalid emails, missing required fields, or phone numbers before submitting).
- Automatic inventory check so customers cannot order out-of-stock products.

### Multi-Step Order Tracking
- Order status tracking for every placed order with 4 visual steps:
  1. Order Placed
  2. Processing
  3. Shipped
  4. Delivered
- Each order tracks its own current status independently.
- Displays estimated delivery dates (4 to 7 days from placement).
- Fully responsive layout so the timeline renders cleanly on mobile screens.

### Invoices and Confirmation
- Automatic order confirmation email after placing an order.
- PDF invoice generation powered by ReportLab with itemized pricing, customer address, and total amount.
- Invoice preview and download buttons available directly from the order success page and user profile.

### Authentication and UI
- User registration, login, logout, and account profile page.
- Dark and Light mode toggle with user preference saved in local storage.
- Responsive mobile burger menu.
- Floating back-to-top button and auto-dismiss toast alerts.

---

## Tech Stack

- Backend: Python, Django
- Frontend: HTML5, CSS3, JavaScript (Fetch API)
- Database: SQLite3
- PDF Generation: ReportLab
- Icons: Font Awesome

---

## Project Structure

```
CodeAlpha_Ecommerce_Store/
|-- ecommerce_store/        # Project settings and core routing
|   |-- settings.py
|   |-- urls.py
|-- store/                  # Main application
|   |-- models.py           # Product, Category, Order, Cart models
|   |-- views.py            # Business logic and views
|   |-- urls.py             # App route definitions
|   |-- forms.py            # Checkout and review forms
|   |-- cart.py             # Session cart handling
|   |-- static/             # CSS styling and JavaScript files
|   |-- templates/          # HTML templates
|-- seed_products.py        # Demo product data loader
|-- requirements.txt        # Python package list
|-- manage.py
|-- README.md
```

---

## How to Run the Project Locally

### 1. Prerequisites
- Python 3.12 or higher installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/pratham2686-patel/CodeAlpha_Ecommerce_Store.git
cd CodeAlpha_Ecommerce_Store
```

### 3. Create a Virtual Environment
- On Windows:
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```
- On macOS / Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. (Optional) Populate Products
The included database already has pre-filled products. If you want to repopulate them, run:
```bash
python seed_products.py
```

### 7. Run the Server
```bash
python manage.py runserver
```

Open your browser and visit: `http://127.0.0.1:8000/`

To access the Django Admin panel, create a superuser:
```bash
python manage.py createsuperuser
```
Then visit: `http://127.0.0.1:8000/admin/`

