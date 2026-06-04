from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductImage, ProductVariant, Review,
    Wishlist, Cart, CartItem, Address, Order, OrderItem,
    Banner, Coupon, UserProfile, SellerProfile
)

admin.site.site_header = "🛒 ShopKaro Admin"
admin.site.site_title = "ShopKaro"
admin.site.index_title = "Welcome to ShopKaro Admin Panel"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'icon', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'alt_text']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'seller', 'price', 'original_price', 'discount_percent',
                    'stock', 'rating', 'is_active', 'is_featured', 'is_bestseller', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_bestseller', 'category', 'condition']
    search_fields = ['name', 'brand', 'sku', 'tags']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'is_bestseller', 'stock', 'price']
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ['total_sold', 'total_reviews', 'rating']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'seller', 'brand', 'condition', 'tags', 'sku')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount_percent')
        }),
        ('Inventory', {
            'fields': ('stock', 'weight')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_bestseller')
        }),
        ('Stats (Read Only)', {
            'fields': ('total_sold', 'total_reviews', 'rating'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'user', 'is_approved', 'is_active', 'rating', 'total_sales', 'created_at']
    list_filter = ['is_approved', 'is_active']
    search_fields = ['shop_name', 'user__username', 'user__email']
    list_editable = ['is_approved', 'is_active']
    actions = ['approve_sellers']

    def approve_sellers(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} sellers approved!")
    approve_sellers.short_description = "Approve selected sellers"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_method', 'payment_status',
                    'total', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status']
    search_fields = ['order_number', 'user__username', 'user__email']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['order_number', 'created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase']
    search_fields = ['product__name', 'user__username']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_editable = ['is_active', 'order']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'min_order_amount',
                    'used_count', 'usage_limit', 'is_active', 'valid_from', 'valid_to']
    list_editable = ['is_active']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'is_seller', 'created_at']
    list_filter = ['is_seller', 'gender']
    search_fields = ['user__username', 'user__email', 'phone']


admin.site.register(ProductImage)
admin.site.register(Address)
admin.site.register(Wishlist)
