# ElectroMart — Django E-Commerce Store

A full-featured e-commerce web application built with **Django**, developed as part of the **CodeAlpha Internship** (Web Development track).

## Features

- **Product Catalog** — browse, search, filter by category, and sort products
- **Product Details** — image, description, stock status, and price with discount badges
- **Shopping Cart** — add / update quantity / remove items instantly via AJAX (no page reloads)
- **Wishlist** — save products for later
- **User Accounts** — register, login, logout, profile page with order history
- **Checkout & Orders** — shipping details form with real-time client-side validation, order confirmation page
- **Order Emails & Invoices** — automatic confirmation email and downloadable PDF invoice per order
- **Product Reviews** — rate and review purchased products; edit/delete your own reviews
- **Dark / Light Theme Toggle**
- **Fully Responsive** — mobile-friendly navigation, layouts, and touch targets

## Tech Stack

- **Backend:** Django 6
- **Database:** SQLite (default, zero-config)
- **Frontend:** HTML, CSS (custom, no framework), vanilla JavaScript (AJAX via `fetch`)
- **PDF Generation:** ReportLab
- **Icons:** Font Awesome

## Project Structure

```
CodeAlpha_E-commerse_store/
├── ecommerce_store/        # Django project settings, URLs, WSGI/ASGI
├── store/                  # Main app
│   ├── models.py           # Category, Product, Cart, Order, Review, Wishlist models
│   ├── views.py            # All view logic (product list, cart, checkout, auth, etc.)
│   ├── forms.py            # Registration, order, review, and cart forms
│   ├── cart.py             # Session-based cart logic
│   ├── admin.py            # Django admin registrations
│   ├── management/commands/seed_products.py   # Seeds 16 extra demo products
│   ├── static/              # CSS and JS
│   └── templates/          # All HTML templates
├── seed_products.py         # Seeds 20 demo products + categories
├── requirements.txt
└── manage.py
```

## Setup Instructions

> **Requires Python 3.12 or newer** (Django 6 does not support older Python versions). Check your version first with `python --version`. If your system Python is older, install Python 3.12+ from [python.org](https://www.python.org/downloads/) before continuing.

1. **Clone / extract the project**, then move into the project folder:
   ```bash
   cd CodeAlpha_E-commerse_store
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
   > A pre-seeded `db.sqlite3` is already included, so this step is mainly a safety check — you should already see products when you run the server.

5. **(Optional) Re-seed demo products** if you start from a fresh database:
   ```bash
   python manage.py seed_products
   ```

6. **Create an admin account** (optional, to access `/admin/`):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. Open **http://127.0.0.1:8000/** in your browser.

## Notes

- `DEBUG = True` and the `SECRET_KEY` in `ecommerce_store/settings.py` are configured for local development only. **Do not use these settings in production** — set `DEBUG = False`, move the secret key to an environment variable, and configure `ALLOWED_HOSTS` before deploying.
- Order confirmation emails use Django's console/SMTP email backend as configured in `settings.py` — update `EMAIL_HOST_USER` and related settings to send real emails.
- Product images are sourced from [Unsplash](https://unsplash.com) for demo purposes.

## Author

Submitted as part of the **CodeAlpha Web Development Internship**.
