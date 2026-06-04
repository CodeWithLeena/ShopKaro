from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.utils import timezone
from .models import (
    Category, Product, ProductImage, Review, Wishlist, Cart, CartItem,
    Address, Order, OrderItem, Banner, Coupon, UserProfile, SellerProfile
)
import json


def home(request):
    banners = Banner.objects.filter(is_active=True)[:5]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    bestseller_products = Product.objects.filter(is_active=True, is_bestseller=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    top_categories = Category.objects.filter(is_active=True, parent=None)[:12]
    deals = Product.objects.filter(is_active=True, discount_percent__gte=30).order_by('-discount_percent')[:6]

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'bestseller_products': bestseller_products,
        'new_arrivals': new_arrivals,
        'top_categories': top_categories,
        'deals': deals,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Filters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'newest')
    brand_filter = request.GET.get('brand', '')
    rating_filter = request.GET.get('rating')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(Q(category=category) | Q(category__parent=category))
    else:
        category = None

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand_filter:
        products = products.filter(brand__icontains=brand_filter)
    if rating_filter:
        products = products.filter(rating__gte=rating_filter)

    # Sorting
    sort_options = {
        'newest': '-created_at',
        'price_low': 'price',
        'price_high': '-price',
        'rating': '-rating',
        'popular': '-total_sold',
        'discount': '-discount_percent',
    }
    products = products.order_by(sort_options.get(sort_by, '-created_at'))

    # Brands for filter
    brands = Product.objects.filter(is_active=True).exclude(brand='').values_list('brand', flat=True).distinct()

    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
        'sort_by': sort_by,
        'brands': brands,
        'total_count': paginator.count,
    }
    return render(request, 'store/product_list.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    request.GET = request.GET.copy()
    request.GET['category'] = slug
    return product_list(request)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:6]
    variants = product.variants.all()

    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, product=product).exists()

    # Rating breakdown
    rating_counts = {}
    for i in range(1, 6):
        rating_counts[i] = reviews.filter(rating=i).count()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to write a review')
            return redirect('login')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        title = request.POST.get('title', '')
        if rating and comment:
            review, created = Review.objects.get_or_create(
                product=product, user=request.user,
                defaults={'rating': rating, 'comment': comment, 'title': title}
            )
            if created:
                avg = product.reviews.aggregate(Avg('rating'))['rating__avg']
                product.rating = round(avg, 2)
                product.total_reviews = product.reviews.count()
                product.save()
                messages.success(request, 'Review submitted successfully!')
            else:
                messages.info(request, 'You have already reviewed this product')

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'related_products': related_products,
        'variants': variants,
        'is_wishlisted': is_wishlisted,
        'rating_counts': rating_counts,
    }
    return render(request, 'store/product_detail.html', context)


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, defaults={'session_key': None})
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


@login_required
def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    context = {'cart': cart, 'items': items}
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))

        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Please login first', 'redirect': '/login/'})

        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} added to cart!',
            'cart_count': cart.total_items
        })
    return JsonResponse({'status': 'error'})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.user.is_authenticated and item.cart.user == request.user:
        item.delete()
        messages.success(request, 'Item removed from cart')
    return redirect('cart')


def update_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
        return JsonResponse({'status': 'success', 'subtotal': float(item.subtotal), 'cart_total': float(item.cart.total_price)})
    return JsonResponse({'status': 'error'})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        status = 'removed'
        message = 'Removed from wishlist'
    else:
        status = 'added'
        message = 'Added to wishlist!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'message': message})
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.all()
    if not items:
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first() or addresses.first()

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method', 'cod')
        coupon_code = request.POST.get('coupon_code', '')

        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
        elif default_address:
            address = default_address
        else:
            messages.error(request, 'Please add a delivery address')
            return redirect('add_address')

        subtotal = cart.total_price
        discount = 0
        delivery_charge = 0 if subtotal >= 499 else 40
        total = subtotal - discount + delivery_charge

        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            subtotal=subtotal,
            discount=discount,
            delivery_charge=delivery_charge,
            total=total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                seller=item.product.seller,
                quantity=item.quantity,
                price=item.product.price,
            )
            item.product.stock -= item.quantity
            item.product.total_sold += item.quantity
            item.product.save()

        cart.items.all().delete()
        messages.success(request, f'Order #{order.order_number} placed successfully!')
        return redirect('order_detail', order_number=order.order_number)

    context = {
        'cart': cart,
        'items': items,
        'addresses': addresses,
        'default_address': default_address,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'store/orders.html', {'orders': user_orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully')
    else:
        messages.error(request, 'Order cannot be cancelled at this stage')
    return redirect('order_detail', order_number=order_number)


@login_required
def add_address(request):
    if request.method == 'POST':
        address = Address.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address_line1=request.POST.get('address_line1'),
            address_line2=request.POST.get('address_line2', ''),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            address_type=request.POST.get('address_type', 'home'),
            is_default=request.POST.get('is_default') == 'on',
        )
        if address.is_default:
            Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)
        messages.success(request, 'Address added successfully!')
        next_url = request.POST.get('next', 'checkout')
        return redirect(next_url)
    return render(request, 'store/add_address.html')


@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        user_profile.phone = request.POST.get('phone', '')
        user_profile.gender = request.POST.get('gender', '')
        if request.FILES.get('profile_pic'):
            user_profile.profile_pic = request.FILES['profile_pic']
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')

    addresses = Address.objects.filter(user=request.user)
    orders_count = Order.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        'user_profile': user_profile,
        'addresses': addresses,
        'orders_count': orders_count,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'store/profile.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_seller = request.POST.get('is_seller') == 'on'

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'store/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'store/register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password1,
            first_name=first_name, last_name=last_name
        )
        UserProfile.objects.create(user=user, is_seller=is_seller)

        if is_seller:
            shop_name = request.POST.get('shop_name', f"{first_name}'s Shop")
            SellerProfile.objects.create(user=user, shop_name=shop_name)

        login(request, user)
        messages.success(request, f'Welcome to ShopKaro, {user.first_name or username}!')
        return redirect('home')

    return render(request, 'store/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next', 'home')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'store/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required
def seller_dashboard(request):
    try:
        seller = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.error(request, 'You are not registered as a seller')
        return redirect('home')

    products = Product.objects.filter(seller=seller)
    total_orders = OrderItem.objects.filter(seller=seller).count()
    total_revenue = sum(item.subtotal for item in OrderItem.objects.filter(seller=seller))
    recent_orders = OrderItem.objects.filter(seller=seller).select_related('order', 'product').order_by('-order__created_at')[:10]

    context = {
        'seller': seller,
        'products': products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'products_count': products.count(),
    }
    return render(request, 'store/seller_dashboard.html', context)


@login_required
def add_product(request):
    try:
        seller = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.error(request, 'You need a seller account to add products')
        return redirect('home')

    if not seller.is_approved:
        messages.warning(request, 'Your seller account is pending approval')
        return redirect('seller_dashboard')

    categories = Category.objects.filter(is_active=True)

    if request.method == 'POST':
        product = Product.objects.create(
            seller=seller,
            category=get_object_or_404(Category, id=request.POST.get('category')),
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            short_description=request.POST.get('short_description', ''),
            price=request.POST.get('price'),
            original_price=request.POST.get('original_price') or None,
            stock=request.POST.get('stock', 0),
            brand=request.POST.get('brand', ''),
            tags=request.POST.get('tags', ''),
        )

        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            ProductImage.objects.create(product=product, image=image, is_primary=(i == 0))

        messages.success(request, 'Product added successfully!')
        return redirect('seller_dashboard')

    return render(request, 'store/add_product.html', {'categories': categories})


def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(tags__icontains=query),
            is_active=True
        )
    else:
        products = Product.objects.none()

    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query,
        'total': paginator.count
    })
