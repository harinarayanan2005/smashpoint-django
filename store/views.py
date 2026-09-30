from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import random
from .models import Product, Category, Order, OrderItem

def home(request):
    category_slug = request.GET.get('category', 'all')
    brand_filter = request.GET.get('brand', 'all')
    price_range = request.GET.get('price', 'all')
    play_style = request.GET.get('style', 'all')
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'featured')

    categories = Category.objects.all()
    products = Product.objects.filter(is_featured=True)

    # 1. Category filter
    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)

    # 2. Brand filter
    if brand_filter and brand_filter != 'all':
        products = products.filter(brand__iexact=brand_filter)

    # 3. Price range filter
    if price_range == 'under_1k':
        products = products.filter(price__lt=1000)
    elif price_range == '1k_10k':
        products = products.filter(price__gte=1000, price__lte=10000)
    elif price_range == '10k_18k':
        products = products.filter(price__gte=10000, price__lte=18000)
    elif price_range == 'above_18k':
        products = products.filter(price__gt=18000)

    # 4. Play style / Balance filter
    if play_style == 'head_heavy':
        products = products.filter(Q(badge__icontains='Heavy') | Q(specs__icontains='Heavy') | Q(description__icontains='head-heavy'))
    elif play_style == 'head_light':
        products = products.filter(Q(badge__icontains='Light') | Q(specs__icontains='Light') | Q(description__icontains='headlight') | Q(description__icontains='head-light'))
    elif play_style == 'control':
        products = products.filter(Q(badge__icontains='Control') | Q(badge__icontains='Surgical') | Q(specs__icontains='Control'))

    # 5. Search filter (name, brand, specs, description, badge)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(specs__icontains=search_query) |
            Q(badge__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # 6. Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-id')

    # Available racquets specifically for the dynamic customizer
    racquet_category = Category.objects.filter(slug='racquets').first()
    all_racquets = Product.objects.filter(category=racquet_category) if racquet_category else []

    available_brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'all_racquets': all_racquets,
        'active_category': category_slug,
        'active_brand': brand_filter,
        'active_price': price_range,
        'active_style': play_style,
        'search_query': search_query,
        'sort_by': sort_by,
        'available_brands': available_brands,
        'total_count': products.count()
    })


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

        # Validations
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'store/register.html', {'next': next_redirect})

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html', {'username': username, 'email': email, 'next': next_redirect})

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'store/register.html', {'username': username, 'email': email, 'next': next_redirect})

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return render(request, 'store/register.html', {'email': email, 'next': next_redirect})

        if email and User.objects.filter(email=email).exists():
            messages.error(request, f'An account with email "{email}" already exists.')
            return render(request, 'store/register.html', {'username': username, 'next': next_redirect})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'Welcome to SmashPoint, {user.username}! Your account has been registered.')
        
        if next_redirect and next_redirect not in ['home', 'None', '']:
            return redirect(next_redirect)
        return redirect('home')

    return render(request, 'store/register.html', {'next': next_url})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_redirect = request.POST.get('next', 'home')

        if not username or not password:
            messages.error(request, 'Please enter your username and password.')
            return render(request, 'store/login.html', {'next': next_redirect})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            if next_redirect and next_redirect not in ['home', 'None', '']:
                return redirect(next_redirect)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'store/login.html', {'next': next_url})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out safely.')
    return redirect('home')


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

        try:
            cart_items = json.loads(cart_data_json)
        except Exception:
            cart_items = []

        if not cart_items:
            messages.error(request, 'Your shopping bag is empty. Please add items before checking out.')
            return redirect('home')

        if not (full_name and phone_number and address and city and state and pincode):
            messages.error(request, 'Please fill in all shipping address fields.')
            return render(request, 'store/checkout.html')

        total_amount = sum(item.get('price', 0) * item.get('qty', 1) for item in cart_items)
        order_id = f"SP-{random.randint(10000, 99999)}"

        # Create Order
        order = Order.objects.create(
            user=request.user,
            order_id=order_id,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            payment_method=payment_method,
            total_amount=total_amount
        )

        # Create Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.get('name', 'Badminton Equipment'),
                price=item.get('price', 0),
                quantity=item.get('qty', 1),
                image_url=item.get('image', '')
            )

        return render(request, 'store/order_success.html', {
            'order': order,
            'items': order.items.all()
        })

    return render(request, 'store/checkout.html')
