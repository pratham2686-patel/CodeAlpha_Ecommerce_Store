# ⚡ ElectroMart — Full-Stack Django E-Commerce Platform

A production-ready, feature-rich E-Commerce web application developed with **Django**, **JavaScript (ES6+)**, and **ReportLab**. Built with modern UX principles featuring asynchronous interactions (no page reload), real-time multi-step order tracking, PDF invoice generation, and full responsive design across desktop and mobile devices.

Developed as a capstone project for the **CodeAlpha Web Development Internship**.

---

## 🚀 Key Features

### 1. 📦 Real-Time Multi-Step Order Tracking
- **Order Progress Stepper:** Dynamic 4-stage tracking timeline (`Pending` ➔ `Processing` ➔ `Shipped` ➔ `Delivered`).
- **Individual Order Status:** Each customer order displays its own independent status, color-coded badge, and estimated delivery dates (4–7 business days).
- **Mobile-Adaptive Tracker:** Automatically scales cleanly from desktop down to compact smartphone screens without overflow.

### 2. ⚡ Smooth Asynchronous (AJAX) User Experience
- **Instant Add-to-Cart:** Click-to-add with spinner and checkmark animation feedback without refreshing the page.
- **In-Place Cart Updates:** Real-time quantity adjustment and item removal using DOM swapping (`cartAjaxRoot`).
- **One-Click Wishlist / Saved Items:** Toggle items into wishlist with animated heart icons and toast notifications.
- **Live Search Autocomplete:** Real-time product suggestions dropdown with thumbnail preview and price while typing (minimum 2 characters).

### 3. 📄 Automated PDF Invoices & Purchase History
- **Download & Preview:** Powered by **ReportLab**, generates official branded tax invoices (`Invoice_Order_#ID.pdf`) with customer details, order itemization, and totals.
- **Order Confirmation Email:** Automatic HTML/text order summary dispatched upon successful checkout.
- **Unified Account Statement:** Download consolidated purchase history report covering all past purchases.

### 4. 🛒 Product Browsing & Filtering
- **Faceted Search & Filters:** Filter products by Category, Price Range (Min/Max), Star Rating (2+, 3+, 4+), and Stock Availability.
- **Sorting Options:** Sort by Newest, Price (Low to High), Price (High to Low), and Highest Rated.
- **Smart Pagination:** Preserves active search queries and filter parameters across page changes.
- **Recently Viewed Items:** Session-based horizontal carousel remembering recently browsed items.

### 5. 🛡️ User Authentication & Validation
- **Secure Authentication:** User registration, session login, logout, and protected customer dashboard.
- **Real-Time Client-Side Validation:** Instant input validation with inline warnings for email format, password strength, and required fields.
- **Database Stock Protection:** Atomic inventory deduction on purchase and prevention of out-of-stock ordering.

### 6. 🎨 Modern Design & UI/UX
- **Dual Theme System:** Instant **Dark / Light** mode toggle with zero-flicker `localStorage` persistence.
- **100% Mobile Responsive:** Slide-out burger menu for mobile, responsive product cards, touch-friendly buttons, and floating Back-to-Top button.
- **Interactive Toasts:** Auto-dismissing floating notification system for alerts and feedback.

---

## 🛠️ Tech Stack

| Component | Technology Used |
|---|---|
| **Backend Framework** | Django 6.x (Python) |
| **Database** | SQLite3 (Configured & Pre-seeded) |
| **Frontend** | Semantic HTML5, Custom Modern CSS3 (CSS Variables, Flexbox/Grid) |
| **Client-side Scripting** | Vanilla JavaScript (ES6+, Fetch API for AJAX) |
| **PDF Generation** | ReportLab 4.x |
| **Icons & Typography** | Font Awesome 6.4, Google Fonts (Outfit & Inter) |
| **Version Control** | Git & GitHub |

---

## 📂 Project Architecture

```
CodeAlpha_Ecommerce_Store/
│
├── ecommerce_store/             # Project configuration & settings
│   ├── settings.py              # App settings, media/static config, email backend
│   ├── urls.py                  # Global URL routing
│   ├── wsgi.py / asgi.py        # Web server interfaces
│
├── store/                       # Core E-Commerce application
│   ├── models.py                # Database models (Category, Product, Order, OrderItem, Wishlist, Review)
│   ├── views.py                 # Controller logic (catalog, cart, checkout, invoice, auth)
│   ├── urls.py                  # Application URL patterns
│   ├── forms.py                 # Django forms & validation
│   ├── cart.py                  # Session-based shopping cart manager
│   ├── context_processors.py    # Global context (cart count, categories)
│   ├── admin.py                 # Django Admin configuration
│   ├── management/commands/     # Custom seed commands
│   ├── static/
│   │   ├── css/styles.css       # Complete design system & responsive media queries
│   │   └── js/main.js           # AJAX handlers, theme switcher, live search, validations
│   └── templates/
│       ├── base.html            # Master layout with navbar, footer & theme scripts
│       └── store/
│           ├── _order_tracker.html   # Reusable responsive order timeline component
│           ├── product_list.html     # Catalog page with filter/sort & pagination
│           ├── product_detail.html   # Product details, reviews & add-to-cart
│           ├── cart_detail.html      # AJAX shopping cart
│           ├── checkout.html         # Billing & shipping form
│           ├── order_success.html    # Order confirmation & delivery estimate
│           ├── profile.html          # User account dashboard & order tracking history
│           ├── wishlist.html         # Saved items page
│           ├── login.html            # Authentication forms
│           └── register.html
│
├── seed_products.py             # Database population script (20 demo products)
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
└── README.md                    # Project documentation
```

---

## ⚙️ Installation & Local Setup

Follow these steps to run the project locally on your machine:

### 1. Prerequisites
- **Python 3.12+** installed on your system ([Download Python](https://www.python.org/downloads/)).
- **Git** installed.

### 2. Clone the Repository
```bash
git clone https://github.com/pratham2686-patel/CodeAlpha_Ecommerce_Store.git
cd CodeAlpha_Ecommerce_Store
```

### 3. Create & Activate Virtual Environment
- **Windows (PowerShell/CMD):**
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```
> **Note:** The included `db.sqlite3` is already pre-configured with sample products and categories.

### 6. (Optional) Re-seed Products
If you ever reset the database, seed fresh products with:
```bash
python seed_products.py
```

### 7. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

Admin portal is accessible at:
👉 **`http://127.0.0.1:8000/admin/`**

---

## 📌 Core User Flows

1. **Shopping & Cart:** Browse products ➔ Filter by price/rating ➔ Add to cart via AJAX without page reload ➔ Update quantities in-place.
2. **Checkout & Order Placement:** Proceed to checkout ➔ Fill address with real-time field validation ➔ Place order ➔ Receive immediate order ID and estimated delivery timeline.
3. **Tracking & Invoices:** Open **Profile** to view all orders ➔ Inspect step-by-step visual tracker for each order ➔ Click **Preview PDF** or **Download PDF** for official invoice bill.
4. **Admin Order Management:** Login to `/admin/` ➔ Change order status from `Processing` to `Shipped` or `Delivered` ➔ Instantly see the customer's visual tracker update.

---

## 👨‍💻 Author

**Pratham Patel**  
- **GitHub:** [@pratham2686-patel](https://github.com/pratham2686-patel)  
- **Project:** CodeAlpha Web Development Internship Program  

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
