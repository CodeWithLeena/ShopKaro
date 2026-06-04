from .models import Category, Cart, CartItem, Wishlist


def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.total_items
        except Cart.DoesNotExist:
            count = 0
    return {'cart_count': count}


def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_count': count}


def categories_processor(request):
    categories = Category.objects.filter(is_active=True, parent=None).prefetch_related('subcategories')
    return {'all_categories': categories}
