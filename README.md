# SMASHPOINT — Pro Badminton E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Three.js](https://img.shields.io/badge/Three.js-WebGL-000000?style=for-the-badge&logo=three.js&logoColor=white)](https://threejs.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org)
[![CSS3](https://img.shields.io/badge/CSS3-Custom_Design_System-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org)

**SMASHPOINT** is a full-stack e-commerce web application engineered for tournament-grade badminton equipment. Built on pure **Django (MVT architecture)**, the platform integrates real-time hardware-accelerated **Three.js WebGL 3D wave aerodynamics**, multi-parameter equipment filtering, persistent shopping cart sessions, an enforced customer authentication gate for purchases, and full checkout and order tracking localized for India.

---

## ⚡ Key Highlights & Features

### 1. 🌊 Interactive 3D Aerodynamic Wave Hero
- **Hardware-Accelerated WebGL**: Custom 3D particle wave simulation built with Three.js that models court aerodynamics and high-velocity shuttlecock smashes.
- **Dynamic Mouse Parallax**: Fluid camera tracking reacting to cursor movement with smooth linear interpolation.
- **Real-Time Dynamic Presets**: Interactive mode controls directly on the hero dashboard:
  - `Calm Drift`: Gentle low-frequency ripple.
  - `Tour Flow`: Balanced tournament-level air displacement.
  - `Smash Turbo`: High-speed 400+ km/h aerodynamic turbulence.
- **Telemetry Display**: Live court benchmark HUD showing world-record smash velocity (493 km/h), electronic string tension limits (35 lbs), and authentic importer guarantees.

### 2. 🏸 Curated Tournament Catalog (29 Items)
- **High-Contrast Illuminated Pods**: Product photography displayed inside ambient, radial white pedestals ensuring dark carbon-fiber frames, grommets, and strings are 100% visible against dark themes.
- **Balanced 4-Column Responsive Grid**: Cards adapt across desktop, tablet, and mobile displays with hover lift and glowing borders.
- **Authentic Brands & Specs**: Real-world equipment spanning **Yonex, Victor, and Li-Ning** across four categories:
  - **Racquets**: Head-heavy attacking, headlight speed, and precision control frames.
  - **Footwear**: Power Cushion+ stability and lightweight tournament court shoes.
  - **Shuttlecocks**: BWF tournament-approved goose feather and durable synthetic nylon shuttles.
  - **Bags & Accessories**: Multi-compartment pro bags, tour strings, and overgrips.

### 3. 🔍 Multi-Parameter Filter Matrix
- Instant filtering without external dependencies:
  - **Category Tabs**: Racquets, Footwear, Shuttlecocks, Bags & Gear.
  - **Brand Selectors**: All, Yonex, Victor, Li-Ning.
  - **Budget Filters**: Under ₹1K, ₹1K–₹10K, ₹10K–₹18K, Above ₹18K.
  - **Balance / Play Style**: Head Heavy, Head Light, Control.
  - **Keyword Search & Sorting**: Real-time search across names, specs, and badges with price/rating sorting.

### 4. 🛒 Slide-Over Shopping Bag Drawer
- Full slide-over drawer cart built on client-side state with instant sync.
- Real-time item stepper (+ / -), automatic subtotal recalculation, and free nationwide express shipping badges.
- Persistent across page reloads and filter changes.

### 5. 🔒 Enforced Checkout Authentication Flow
- **Purchase Protection**: Direct checkout and **"Buy Now"** actions require customer authentication.
- **Smart Redirection**:
  - **Existing Players**: Redirected to `/login/?next=/checkout/` $\rightarrow$ signs in $\rightarrow$ sent directly to checkout.
  - **New Visitors**: Can click **"Create an Account"** on the gatekeeper banner $\rightarrow$ registers account $\rightarrow$ auto-authenticated $\rightarrow$ seamlessly forwarded to complete order.
  - **Logged-in Customers**: Proceed immediately to order completion without interruption.

### 6. 📦 Checkout & Database Order Processing
- Complete shipping address form tailored for Indian postal logistics (Street, City, State dropdown, 6-digit PIN code, Contact Number).
- Flexible payment methods:
  - ⚡ **Instant UPI / QR** (Google Pay, PhonePe, Paytm, BHIM)
  - 💳 **Credit / Debit Cards & NetBanking**
  - 📦 **Cash on Delivery (COD)**
- Database records generated in real-time (`Order` and itemized `OrderItem` rows).
- Printable, itemized order invoice screen (`order_success.html`) with order reference code and automatic cart clearing.

### 7. 🛠️ Administrative Portal
- Accessible at `/admin/` with custom equipment thumbnails, category metrics, and customer order fulfillment status tracking.

---

## 💻 Tech Stack & Skills Demonstrated

| Technology | Role in Project |
| :--- | :--- |
| **Python 3.11+** | Backend core and business logic |
| **Django 5.2+** | Full-stack framework (MVT: Models, Views, Templates), ORM queries, authentication system, flash messaging |
| **SQLite3** | Relational database modeling Categories, Products, Orders, and OrderItems |
| **JavaScript (ES6+)** | Dynamic DOM rendering, cart management, modal drawers, and URL parameter handling |
| **Three.js (WebGL)** | 3D procedural wave math, custom buffer geometry, vertex shaders, and mouse parallax |
| **Vanilla CSS3** | Custom dark cyber-court design system, CSS Grid, Flexbox, glassmorphism (`backdrop-filter`), animations |

---

## 📂 Project Structure

```text
badminton_store/
├── manage.py                     # Django management CLI
├── requirements.txt              # Project dependencies
├── .gitignore                    # Version control exclusions
├── README.md                     # Documentation
├── db.sqlite3                    # Pre-populated database with 29 products
├── badminton_store/              # Project Configuration
│   ├── __init__.py
│   ├── settings.py               # Django configuration & static paths
│   ├── urls.py                   # Master URL routing
│   ├── asgi.py
│   └── wsgi.py
└── store/                        # Core Application
    ├── admin.py                  # Admin models & custom image thumbnails
    ├── apps.py
    ├── models.py                 # Category, Product, Order, OrderItem models
    ├── views.py                  # Catalog, Cart, Auth, and Checkout controllers
    ├── urls.py                   # Store URL endpoints
    ├── static/
    │   ├── css/
    │   │   └── style.css         # Complete responsive design system
    │   ├── js/
    │   │   ├── three.min.js      # Three.js WebGL engine
    │   │   └── hero_wave.js      # 3D interactive wave animation script
    │   └── images/               # High-res studio equipment images (PNG)
    └── templates/
        └── store/
            ├── home.html         # Homepage with 3D wave & catalog grid
            ├── login.html        # Player authentication gate
            ├── register.html     # New player registration
            ├── checkout.html     # Shipping & payment gateway
            └── order_success.html# Itemized order confirmation invoice
```

---

## 🚀 Quick Setup & Installation Guide

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/badminton-store.git
cd badminton-store
```

### 2. Create and Activate Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

---

## 📦 Adding to Git & Pushing to GitHub

To push this repository to your personal GitHub account:

```bash
# 1. Initialize git (if not already initialized)
git init

# 2. Add all project files
git add .

# 3. Commit changes
git commit -m "Initial commit: SMASHPOINT Pro Badminton E-Commerce Platform"

# 4. Rename main branch
git branch -M main

# 5. Link to your GitHub repository
git remote add origin https://github.com/your-username/your-repo-name.git

# 6. Push to GitHub
git push -u origin main
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
