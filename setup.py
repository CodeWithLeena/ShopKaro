#!/usr/bin/env python
"""
ShopKaro - Auto Setup Script
Run this ONCE after installing requirements:
    python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopkaro.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, ProductImage, Banner, UserProfile, SellerProfile

print("\n" + "="*50)
print("  🛒 ShopKaro - Auto Setup")
print("="*50)

# 1. RUN MIGRATIONS
print("\n[1/4] Running database migrations...")
from django.core.management import call_command
call_command('makemigrations', '--verbosity=0')
call_command('migrate', '--verbosity=0')
print("    ✅ Database ready!")

# 2. CREATE SUPERUSER
print("\n[2/4] Creating admin user...")
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@shopkaro.com', 'admin123')
    UserProfile.objects.create(user=admin, is_seller=False)
    print("    ✅ Admin created! (username: admin | password: admin123)")
else:
    print("    ℹ️  Admin already exists")

# 3. CREATE CATEGORIES
print("\n[3/4] Creating categories...")
categories_data = [
    # (name, icon, subcategories)
    ("Electronics", "fa-laptop", ["Mobile Phones", "Laptops", "Tablets", "Cameras", "Headphones", "Smartwatches", "TVs", "Speakers"]),
    ("Fashion", "fa-tshirt", ["Men's Clothing", "Women's Clothing", "Kids' Fashion", "Footwear", "Accessories", "Bags & Wallets", "Ethnic Wear", "Sportswear"]),
    ("Home & Living", "fa-home", ["Furniture", "Kitchen & Dining", "Bedding", "Decor", "Garden", "Storage", "Lighting", "Bath"]),
    ("Beauty & Health", "fa-spa", ["Skincare", "Haircare", "Makeup", "Fragrances", "Health Devices", "Vitamins", "Personal Care", "Baby Care"]),
    ("Books & Stationery", "fa-book", ["Fiction", "Non-Fiction", "Academic", "Comics & Manga", "Children's Books", "Notebooks", "Art Supplies"]),
    ("Sports & Outdoors", "fa-football-ball", ["Cricket", "Football", "Badminton", "Cycling", "Gym & Fitness", "Yoga", "Camping", "Swimming"]),
    ("Toys & Games", "fa-gamepad", ["Action Figures", "Board Games", "Educational Toys", "Remote Control", "Dolls", "Building Blocks", "Video Games"]),
    ("Grocery & Food", "fa-shopping-basket", ["Dry Fruits", "Snacks", "Beverages", "Organic", "Dairy", "Bakery", "Spices", "Instant Food"]),
    ("Automotive", "fa-car", ["Car Accessories", "Bike Accessories", "Helmets", "Car Care", "Tools", "Spare Parts"]),
    ("Jewellery", "fa-gem", ["Gold Jewellery", "Silver Jewellery", "Earrings", "Necklaces", "Bangles", "Rings", "Watches"]),
    ("Furniture", "fa-couch", ["Sofas", "Beds", "Tables", "Chairs", "Wardrobes", "Shelves"]),
    ("Pet Supplies", "fa-paw", ["Dog Food", "Cat Food", "Pet Toys", "Grooming", "Cages & Accessories"]),
]

cat_objects = {}
for cat_name, icon, subs in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_name,
        defaults={'icon': icon, 'description': f'Shop the best {cat_name} products'}
    )
    cat_objects[cat_name] = cat
    for sub_name in subs:
        Category.objects.get_or_create(
            name=sub_name,
            defaults={'parent': cat, 'icon': icon}
        )
    if created:
        print(f"    ✅ {cat_name} + {len(subs)} subcategories")

# 4. CREATE SAMPLE PRODUCTS
print("\n[4/4] Creating sample products...")

# Create a demo seller
if not User.objects.filter(username='seller1').exists():
    seller_user = User.objects.create_user('seller1', 'seller@shopkaro.com', 'seller123', first_name='Demo', last_name='Seller')
    UserProfile.objects.create(user=seller_user, is_seller=True)
    seller_profile = SellerProfile.objects.create(
        user=seller_user,
        shop_name='ShopKaro Official Store',
        description='Official demo store',
        is_approved=True,
        rating=4.5
    )
else:
    seller_profile = SellerProfile.objects.filter(user__username='seller1').first()

sample_products = [
    # Electronics
    {
        'name': 'Samsung Galaxy A54 5G Smartphone',
        'category': 'Mobile Phones',
        'price': 28999, 'original_price': 38999,
        'stock': 50, 'brand': 'Samsung',
        'rating': 4.3, 'total_reviews': 2847, 'total_sold': 5620,
        'is_featured': True, 'is_bestseller': True,
        'short_description': '6.4" Super AMOLED Display | 50MP Camera | 5000mAh Battery | 8GB RAM | 128GB Storage',
        'description': 'Samsung Galaxy A54 5G comes with an impressive 6.4-inch Super AMOLED display with 120Hz refresh rate. Powered by Exynos 1380 processor with 8GB RAM and 128GB expandable storage. Features a 50MP main camera with OIS, 12MP ultra-wide, and 5MP macro lens. 5000mAh battery with 25W fast charging. IP67 water resistance.',
        'tags': 'smartphone, samsung, 5g, android, mobile phone',
    },
    {
        'name': 'boAt Rockerz 450 Wireless Headphones',
        'category': 'Headphones',
        'price': 1299, 'original_price': 3990,
        'stock': 200, 'brand': 'boAt',
        'rating': 4.1, 'total_reviews': 15230, 'total_sold': 45000,
        'is_featured': True, 'is_bestseller': True,
        'short_description': '15 Hours Battery | 40mm Drivers | Soft Ear Cushions | Built-in Mic',
        'description': 'boAt Rockerz 450 is a wireless headphone with 40mm dynamic drivers for deep bass. Up to 15 hours of battery life. Padded ear cushions for long listening sessions. Built-in mic for calls. Compatible with all Bluetooth devices. Foldable design for easy storage.',
        'tags': 'headphones, wireless, bluetooth, boat, audio',
    },
    {
        'name': 'HP Pavilion 15 Laptop Intel Core i5',
        'category': 'Laptops',
        'price': 49990, 'original_price': 65000,
        'stock': 25, 'brand': 'HP',
        'rating': 4.4, 'total_reviews': 892, 'total_sold': 1240,
        'is_featured': True,
        'short_description': 'Intel Core i5-1235U | 8GB DDR4 | 512GB SSD | 15.6" FHD | Windows 11',
        'description': 'HP Pavilion 15 is a powerful laptop for everyday computing and entertainment. Features Intel Core i5-1235U 12th Gen processor, 8GB DDR4 RAM, 512GB NVMe SSD storage. 15.6-inch Full HD anti-glare display. Windows 11 Home pre-installed. Backlit keyboard, HD webcam, dual speakers with Bang & Olufsen tuning.',
        'tags': 'laptop, hp, intel, windows, computer',
    },
    # Fashion
    {
        'name': 'Roadster Men\'s Slim Fit Jeans',
        'category': "Men's Clothing",
        'price': 799, 'original_price': 1999,
        'stock': 300, 'brand': 'Roadster',
        'rating': 4.2, 'total_reviews': 4521, 'total_sold': 12000,
        'is_featured': True, 'is_bestseller': True,
        'short_description': 'Slim Fit | Mid Rise | Stretch Denim | Available in 28-38 waist sizes',
        'description': 'Roadster Slim Fit Jeans made from high-quality stretch denim for comfort and style. Mid-rise design with zip fly. 5-pocket styling. Machine washable. Suitable for casual and semi-formal occasions. Available in multiple colors and sizes.',
        'tags': 'jeans, men, slim fit, denim, casual',
    },
    {
        'name': 'Libas Women Anarkali Kurta Set',
        'category': 'Ethnic Wear',
        'price': 1299, 'original_price': 2999,
        'stock': 150, 'brand': 'Libas',
        'rating': 4.5, 'total_reviews': 3280, 'total_sold': 8900,
        'is_featured': True,
        'short_description': 'Pure Cotton | Floral Print | Comes with Dupatta | Sizes XS to 3XL',
        'description': 'Beautiful Anarkali Kurta set by Libas made from pure cotton fabric. Featuring elegant floral print with contrast dupatta. A-line silhouette with quarter sleeves. Suitable for festivals, weddings, and casual occasions. Easy care machine washable fabric.',
        'tags': 'kurta, ethnic, women, cotton, anarkali',
    },
    {
        'name': 'Nike Air Max 270 Running Shoes',
        'category': 'Footwear',
        'price': 8495, 'original_price': 12995,
        'stock': 80, 'brand': 'Nike',
        'rating': 4.6, 'total_reviews': 1560, 'total_sold': 3400,
        'is_bestseller': True,
        'short_description': 'Air Max Cushioning | Mesh Upper | Available in sizes 6-11 | Lightweight',
        'description': 'Nike Air Max 270 features the first-ever Max Air unit created specifically for Nike Sportswear. The large Air unit delivers an extremely smooth ride and exceptional comfort for all-day wear. Lightweight mesh upper for breathability. Foam midsole for cushioning.',
        'tags': 'shoes, nike, running, sports, sneakers',
    },
    # Home & Living
    {
        'name': 'Pigeon Smart Glass 1.5L Electric Kettle',
        'category': 'Kitchen & Dining',
        'price': 699, 'original_price': 1499,
        'stock': 500, 'brand': 'Pigeon',
        'rating': 4.3, 'total_reviews': 8750, 'total_sold': 25000,
        'is_bestseller': True,
        'short_description': '1500W | Auto Shut-Off | Boil Dry Protection | Glass Body | 1.5L Capacity',
        'description': 'Pigeon Smart Glass Electric Kettle with 1500W heating element boils water in just 3-4 minutes. Transparent glass body to see water level. Automatic shut-off and boil-dry protection for safety. 360-degree cordless base for convenience. BPA-free food-grade materials.',
        'tags': 'kettle, kitchen, electric, pigeon, appliance',
    },
    # Beauty
    {
        'name': 'Lakme Absolute Perfect Radiance Serum',
        'category': 'Skincare',
        'price': 399, 'original_price': 599,
        'stock': 400, 'brand': 'Lakme',
        'rating': 4.0, 'total_reviews': 2100, 'total_sold': 6500,
        'is_featured': True,
        'short_description': '30ml | Vitamin C | SPF 15 | For All Skin Types | Non-Greasy',
        'description': 'Lakme Absolute Perfect Radiance Serum enriched with Vitamin C and niacinamide helps reduce dark spots and gives radiant skin. Lightweight non-greasy formula absorbs quickly. Suitable for all skin types. Dermatologically tested.',
        'tags': 'serum, skincare, lakme, vitamin c, face care',
    },
    # Sports
    {
        'name': 'Yonex Arcsaber 71 Badminton Racket',
        'category': 'Badminton',
        'price': 2499, 'original_price': 3500,
        'stock': 100, 'brand': 'Yonex',
        'rating': 4.5, 'total_reviews': 678, 'total_sold': 1890,
        'is_featured': True,
        'short_description': 'Isometric Head | Graphite Frame | 85g | Comes with Full Cover',
        'description': 'Yonex Arcsaber 71 Light badminton racket with isometric head shape for larger sweet spot. Graphite frame for lightweight strength. Recommended string tension 20-27 lbs. Comes with full cover. Ideal for intermediate and advanced players.',
        'tags': 'badminton, yonex, racket, sports, outdoor',
    },
    # Grocery
    {
        'name': 'Himalaya Pure Honey 500g',
        'category': 'Organic',
        'price': 299, 'original_price': 399,
        'stock': 1000, 'brand': 'Himalaya',
        'rating': 4.4, 'total_reviews': 5600, 'total_sold': 18000,
        'is_bestseller': True,
        'short_description': '100% Pure | No Added Sugar | Tested for Antibiotics | 500g Pack',
        'description': 'Himalaya Pure Honey is 100% natural honey sourced from Indian forests. No added sugar, preservatives, or artificial flavors. Rich in antioxidants and enzymes. Tested for antibiotics and heavy metals. Suitable for daily consumption.',
        'tags': 'honey, organic, himalaya, grocery, natural',
    },
]

created_count = 0
for p_data in sample_products:
    cat_name = p_data.pop('category')
    try:
        category = Category.objects.get(name=cat_name)
    except Category.DoesNotExist:
        continue

    product, created = Product.objects.get_or_create(
        name=p_data['name'],
        defaults={
            'category': category,
            'seller': seller_profile,
            **{k: v for k, v in p_data.items() if k != 'name'}
        }
    )
    if created:
        created_count += 1

print(f"    ✅ {created_count} sample products created!")

print("\n" + "="*50)
print("  ✅ ShopKaro Setup Complete!")
print("="*50)
print("\n📋 HOW TO RUN:")
print("   cd shopkaro")
print("   python manage.py runserver")
print("\n🔐 ADMIN PANEL: http://127.0.0.1:8000/admin/")
print("   Username: admin")
print("   Password: admin123")
print("\n🛒 WEBSITE: http://127.0.0.1:8000/")
print("\n🏪 SELLER ACCOUNT:")
print("   Username: seller1")
print("   Password: seller123")
print("\n💡 TIPS:")
print("   - Admin panel se products, categories, banners manage karo")
print("   - Seller dashboard: http://127.0.0.1:8000/seller/dashboard/")
print("   - Product images add karne ke liye admin panel use karo")
print("="*50 + "\n")
