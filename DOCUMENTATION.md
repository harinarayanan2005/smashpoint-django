# SMASHPOINT — Technical Architecture & Implementation Documentation

---

## 1. Executive Summary & Project Overview

**SMASHPOINT** is a tournament-grade badminton e-commerce web platform engineered using the **Django Full-Stack (MVT)** architecture, **JavaScript (ES6+)**, and **Three.js (WebGL)**. 

The application is tailored for high-performance sports equipment retail (racquets, court footwear, feather and synthetic shuttles, kitbags, and strings) across India. It balances visual design with backend data modeling, database persistence, and an authentication gatekeeper for checkout workflows.

---

## 2. System Architecture & High-Level Flow

The application follows Django's standard **Model-View-Template (MVT)** pattern:

```
[ Browser Client ]
       │
       ▼  (HTTP Request)
[ urls.py ] ──────────► Routes URL to specific View Function
       │
       ▼
[ views.py ] ◄────────► Interacts with [ models.py ] (ORM Queries to SQLite)
       │
       ▼  (Prepares Context & Renders)
[ templates/*.html ] ──► Injects Static CSS, JS (Three.js WebGL), & Image Assets
       │
       ▼  (HTTP Response)
[ Rendered Webpage to User ]
```

---

## 3. Deep Dive: `store/models.py` (Database Layer)

The database schema is defined in `store/models.py` using Django’s Object-Relational Mapping (ORM) and persists in an SQLite database (`db.sqlite3`).

### 3.1. `Category` Model
Represents the major equipment departments in the store.
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
```
* **Why it is used**: Allows categories to be queried dynamically. The `slug` field provides clean, URL-safe identifiers (e.g., `racquets`, `footwear`, `shuttlecocks`, `bags-gear`).

---

### 3.2. `Product` Model
Represents each individual piece of badminton gear (29 curated items in the catalog).
```python
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=100, default='Yonex')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500)
    description = models.TextField()
    specs = models.CharField(max_length=100, default="4U/G5 • Stiff • 30 LBS")
    badge = models.CharField(max_length=50, default="Head-Heavy")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.9)
    is_featured = models.BooleanField(default=True)
```
* **Why each field is used**:
  - `category`: Establishes a 1-to-many relationship using a ForeignKey. Deleting a category cascades to its products.
  - `image_url`: Stores the relative path to the image asset (e.g., `images/astrox99pro.png`).
  - `specs`: Stores key tournament metrics (weight class `4U`, grip `G5`, flex `Stiff`, max tension `30 LBS`).
  - `badge`: Powers the high-visibility tags (`HYBRID SPIN CUT`, `FORGED REPULSION`, `HEAD-HEAVY`).
  - `price`: Uses `DecimalField` for financial precision in Indian Rupees (`₹`), avoiding floating-point rounding errors.

---

### 3.3. `Order` & `OrderItem` Models
Captures completed customer orders and shipping records.
```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=25, unique=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50, default='UPI')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Confirmed (Processing)')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.CharField(max_length=500, blank=True)
```
* **Why it is used**:
  - Connects orders directly to Django's authenticated `User`.
  - Captures shipping logistics localized for Indian postal addresses.
  - The separate `OrderItem` model retains a snapshot of what was purchased (name, price, qty), preserving invoice integrity even if future product details change.

---

## 4. Deep Dive: `store/urls.py` (Routing Layer)

`store/urls.py` directs incoming browser requests to their respective Python view handlers.

```python
from django.urls import path
from . import views

urlpatterns = [
    # 1. Main Home / Catalog
    path('', views.home, name='home'),

    # 2. Friendly Category URLs (Singular & Plural)
    path('racket/', views.home, {'category_slug': 'racquets'}, name='racket'),
    path('rackets/', views.home, {'category_slug': 'racquets'}, name='rackets'),
    path('racquet/', views.home, {'category_slug': 'racquets'}, name='racquet'),
    path('racquets/', views.home, {'category_slug': 'racquets'}, name='racquets'),

    path('footwear/', views.home, {'category_slug': 'footwear'}, name='footwear'),
    path('shoes/', views.home, {'category_slug': 'footwear'}, name='shoes'),
    path('shoe/', views.home, {'category_slug': 'footwear'}, name='shoe'),

    path('shuttlecocks/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttlecocks'),
    path('shuttlecock/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttlecock'),
    path('shuttles/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttles'),
    path('shuttle/', views.home, {'category_slug': 'shuttlecocks'}, name='shuttle'),

    path('bags-gear/', views.home, {'category_slug': 'bags-gear'}, name='bags_gear'),
    path('bags/', views.home, {'category_slug': 'bags-gear'}, name='bags'),
    path('gear/', views.home, {'category_slug': 'bags-gear'}, name='gear'),
    path('bag/', views.home, {'category_slug': 'bags-gear'}, name='bag'),

    path('category/<slug:category_slug>/', views.home, name='category_filter'),

    # 3. Authentication & Account
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # 4. Checkout
    path('checkout/', views.checkout, name='checkout'),
]
```

### Why this design was chosen:
1. **Friendly, Human-Readable URLs**: Instead of forcing users or search engines to use complex query parameters like `/?category=racquets`, visitors can directly type `/racket/`, `/shoes/`, or `/shuttles/`.
2. **Keyword Arguments (`{'category_slug': 'racquets'}`)**: Passing an extra dictionary argument into `path()` allows multiple URL patterns to reuse the same robust `views.home` controller without duplicate code.
3. **Named Routes (`name='...'`)**: Used across templates (`{% url 'login' %}`) so URLs can be refactored in the future without breaking template hyperlinks.

---

## 5. Deep Dive: `store/views.py` (Controller Logic)

`store/views.py` contains the core business logic, handling search, multi-filtering, user authentication, session security, and checkout transaction handling.

### 5.1. `home(request, category_slug=None)`
```python
CATEGORY_ALIASES = {
    'racket': 'racquets', 'rackets': 'racquets', 'racquet': 'racquets', 'racquets': 'racquets',
    'footwear': 'footwear', 'shoes': 'footwear', 'shoe': 'footwear',
    'shuttlecock': 'shuttlecocks', 'shuttlecocks': 'shuttlecocks', 'shuttle': 'shuttlecocks', 'shuttles': 'shuttlecocks',
    'bag': 'bags-gear', 'bags': 'bags-gear', 'gear': 'bags-gear', 'bags-gear': 'bags-gear',
}
```
* **Step-by-step logic**:
  1. Checks if `category_slug` was supplied via the URL or from `request.GET.get('category')`.
  2. Resolves aliases through `CATEGORY_ALIASES.get(slug)`.
  3. Extracts filter criteria: `brand`, `price`, `style`, `q` (search query), and `sort`.
  4. Executes optimized ORM queries:
     - **Category**: `products.filter(category__slug=category_slug)`
     - **Brand**: `products.filter(brand__iexact=brand_filter)`
     - **Price Tier**: `products.filter(price__gte=..., price__lte=...)`
     - **Play Style / Balance**: Uses `Q` objects (`Q(badge__icontains=...) | Q(specs__icontains=...)`) to match head-heavy, head-light, or control racquets.
     - **Search Query**: Multi-field search across model name, brand, specs, badge, and description.
     - **Sorting**: Evaluates order by price low/high or top player rating.
  5. Renders `store/home.html` with all products and active filter states.

---

### 5.2. `user_register(request)`
```python
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        next_redirect = request.POST.get('next', 'home')
        ...
```
* **Why it is used**:
  - Validates password length (minimum 6 characters) and confirmation match.
  - Checks if the username or email is already registered, rendering user-friendly flash alert messages.
  - Automatically logs in the player via `login(request, user)` upon successful registration.
  - **Redirect Forwarding**: If `next` equals `/checkout/`, the newly registered player is instantly redirected to the checkout page with their shopping bag intact!

---

### 5.3. `user_login(request)` & `user_logout(request)`
```python
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    ...
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next_redirect and next_redirect not in ['home', 'None', '']:
            return redirect(next_redirect)
        return redirect('home')
```
* **Why it is used**:
  - Uses Django's secure `authenticate()` method which performs salted password hash comparison.
  - Respects the `?next=` URL parameter to return users to wherever they were trying to go before authentication.
  - `user_logout` safely destroys the session and redirects home.

---

### 5.4. `checkout(request)`
```python
@login_required(login_url='/login/?next=/checkout/')
def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'UPI')
        cart_data_json = request.POST.get('cart_data', '[]')
        ...
```
* **Why it is used**:
  - Protected with the `@login_required` decorator. If an unauthenticated user attempts to reach checkout, Django redirects them to `/login/?next=/checkout/`.
  - Deserializes JSON shopping bag data passed from `localStorage`.
  - Validates Indian shipping address inputs.
  - Generates a unique reference ID (e.g. `SP-84291`).
  - Creates the `Order` record and loops over the items to create `OrderItem` records in SQLite.
  - Renders `order_success.html` displaying the official invoice, which executes a JavaScript trigger to clear the customer's shopping bag.

---

## 6. How Static Files & Product Images Work

### 6.1. Settings & Directory Layout
In `badminton_store/settings.py`:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'store' / 'static',
]
```
All physical image files live in:
`D:\PROJECTS\badminton_store\store\static\images\`
- Examples: `astrox99pro.png`, `as40.png`, `shb65z3.png`, `aerobiteboost.png`.

### 6.2. How Images Are Referenced in Templates
In the database, `product.image_url` stores the relative path `images/astrox99pro.png`.
In `store/templates/store/home.html`, the image is rendered via:
```html
<div class="product-image-box">
    <img src="/static/{{ product.image_url }}" alt="{{ product.name }}" class="product-img" loading="lazy">
</div>
```
When Django renders the template, it outputs:
```html
<img src="/static/images/astrox99pro.png" alt="Yonex Astrox 99 Pro (White Tiger)" class="product-img">
```

### 6.3. The "Illuminated Studio Pod" Design Rationale
* **The Problem**: Professional badminton racquets feature matte black carbon-fiber weaves, ultra-thin grommets, and dark micro-strings. Placing them directly on dark navy cards causes them to blend in and disappear.
* **The Solution**: Every product image sits inside `.product-image-box` styled with:
  ```css
  background: radial-gradient(circle at center, #ffffff 45%, #f1f5f9 100%) !important;
  border-radius: 12px;
  ```
  This creates an illuminated studio product pedestal with soft drop shadows (`filter: drop-shadow(...)`), giving 100% frame and string visibility.

---

## 7. Real-Time 3D WebGL Wave Simulation (`hero_wave.js`)

Instead of static photos, the hero features a real-time hardware-accelerated 3D wave simulation powered by **Three.js**.

### 7.1. Wave Mathematics
The wave creates an undulating particle matrix using multi-frequency sinusoidal displacement:
$$y(x, z, t) = \sin(x \cdot 0.16 + t) \cdot 24 + \cos(z \cdot 0.18 + t \cdot 0.75) \cdot 18 + \sin((x+z) \cdot 0.09 + t \cdot 1.2) \cdot 11$$

### 7.2. Dynamic Vertex Colors
Points are generated with a `THREE.BufferGeometry` having separate `position` and `color` float arrays. As the wave crests rise and fall:
- Troughs: Deep electric blue (`#3b82f6`).
- Peaks: High-energy luminous cyan (`#00f2fe`) and neon magenta.

### 7.3. Interactive Controls & Mouse Parallax
- The camera position eases towards the mouse cursor using linear interpolation:
  `camera.position.x += (mouseX - camera.position.x) * 0.03;`
- Users can switch wave turbulence modes directly using:
  - `setWavePreset('calm')` — gentle ripple.
  - `setWavePreset('flow')` — tournament air dynamics.
  - `setWavePreset('smash')` — high-speed 400+ km/h smash turbulence.

---

## 8. Summary of All User Flows

```
[ Visitor Browsing ]
         │
         ├──► Filters by Brand/Category/Price (/racket/, /footwear/, /shuttles/)
         ├──► Adjusts 3D Wave Dynamics (Calm, Flow, Smash)
         │
         ▼
[ Adds Items to Cart / Clicks 'Buy Now' ]
         │
         ▼
[ Authentication Gate Check ]
         │
         ├─── Not Logged In ───► Redirects to /login/?next=/checkout/
         │                             │
         │                             ├── Existing User: Signs In ──► Redirects to /checkout/
         │                             │
         │                             └── New User: Registers ──────► Auto-login ──► Redirects to /checkout/
         │
         └─── Already Logged In ────────────────────────────────────► Opens /checkout/
                                                                            │
                                                                            ▼
                                                      [ Enters Indian Address & Payment Mode ]
                                                                            │
                                                                            ▼
                                                      [ Order Placed -> Database Order Stored ]
                                                                            │
                                                                            ▼
                                                      [ Itemized Invoice Rendered -> Cart Reset ]
```

---

## 9. Conclusion
SMASHPOINT represents a complete, cohesive full-stack web application. It combines performance-optimized Django backend logic, relational data modeling, client-side session persistence, and modern WebGL 3D graphics into a unified e-commerce experience.
