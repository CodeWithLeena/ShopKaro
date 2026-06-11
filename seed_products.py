#!/usr/bin/env python
"""
ShopKaro - Auto Product Seeder with Placeholder Images
Run: python3 seed_products.py
"""
import os
import sys
import django
import urllib.request
import ssl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopkaro.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from store.models import Category, Product, ProductImage, SellerProfile
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

print("\n" + "="*60)
print("  ShopKaro - Auto Product Seeder")
print("="*60)

try:
    seller = SellerProfile.objects.filter(is_approved=True).first()
    if not seller:
        user = User.objects.filter(is_superuser=True).first()
        if user:
            seller = SellerProfile.objects.create(
                user=user, shop_name='ShopKaro Official',
                is_approved=True, rating=4.5
            )
except:
    seller = None

def get_category(name, parent_name=None, icon='fa-tag'):
    parent = None
    if parent_name:
        parent, _ = Category.objects.get_or_create(name=parent_name, defaults={'icon': icon})
    cat, _ = Category.objects.get_or_create(name=name, defaults={'parent': parent, 'icon': icon})
    return cat

def download_image(url, product):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as r:
            img_temp = NamedTemporaryFile(delete=True, suffix='.jpg')
            img_temp.write(r.read())
            img_temp.flush()
            if not ProductImage.objects.filter(product=product, is_primary=True).exists():
                pi = ProductImage(product=product, is_primary=True)
                pi.image.save(f"{product.slug}.jpg", File(img_temp))
                pi.save()
                return True
    except Exception as e:
        return False
    return False

def add_product(d):
    cat = get_category(d['category'], d.get('parent_category'), d.get('icon', 'fa-tag'))
    product, created = Product.objects.get_or_create(
        name=d['name'],
        defaults={
            'category': cat, 'seller': seller,
            'description': d['description'],
            'short_description': d.get('short_description', ''),
            'price': d['price'],
            'original_price': d.get('original_price'),
            'stock': d.get('stock', 50),
            'brand': d.get('brand', ''),
            'rating': d.get('rating', 4.0),
            'total_reviews': d.get('reviews', 100),
            'total_sold': d.get('sold', 500),
            'is_active': True,
            'is_featured': d.get('featured', False),
            'is_bestseller': d.get('bestseller', False),
            'tags': d.get('tags', ''),
            'condition': 'new',
        }
    )
    if created or not ProductImage.objects.filter(product=product).exists():
        url = d.get('image_url', '')
        if url:
            ok = download_image(url, product)
            status = "with image" if ok else "no image"
        else:
            status = "no image"
        print(f"  {'Added' if created else 'Updated'} ({status}): {d['name']}")
    else:
        print(f"  Exists: {d['name']}")

products = [
    {
        'name': 'Samsung Galaxy S23 Ultra 5G',
        'category': 'Mobile Phones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 99999, 'original_price': 124999, 'brand': 'Samsung',
        'stock': 30, 'rating': 4.7, 'reviews': 3420, 'sold': 8900,
        'featured': True, 'bestseller': True,
        'image_url': 'https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s23-ultra-5g-1.jpg',
        'short_description': '200MP Camera | 12GB RAM | 256GB | S-Pen | 5000mAh',
        'description': 'Samsung Galaxy S23 Ultra 5G with 200MP main camera, built-in S-Pen, 12GB RAM, 256GB storage.',
        'tags': 'samsung, smartphone, 5g, android',
    },
    {
        'name': 'iPhone 15 128GB Black',
        'category': 'Mobile Phones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 79999, 'original_price': 89900, 'brand': 'Apple',
        'stock': 25, 'rating': 4.8, 'reviews': 5621, 'sold': 12000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-1.jpg',
        'short_description': 'A16 Bionic | 48MP Camera | Dynamic Island | USB-C',
        'description': 'Apple iPhone 15 with A16 Bionic chip, 48MP main camera, Dynamic Island, USB-C connectivity.',
        'tags': 'iphone, apple, smartphone, ios',
    },
    {
        'name': 'boAt Airdopes 141 TWS Earbuds',
        'category': 'Headphones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 999, 'original_price': 3990, 'brand': 'boAt',
        'stock': 500, 'rating': 4.1, 'reviews': 25000, 'sold': 85000,
        'bestseller': True,
        'image_url': 'https://www.boat-lifestyle.com/cdn/shop/products/Airdopes141_1.jpg',
        'short_description': '42 Hours Playback | ENx Tech | BEAST Mode | IPX4',
        'description': 'boAt Airdopes 141 TWS earbuds with 42 hours total playback, ENx technology for clear calls.',
        'tags': 'earbuds, tws, wireless, boat, bluetooth',
    },
    {
        'name': 'Lenovo IdeaPad Slim 3 Laptop Core i3',
        'category': 'Laptops', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 37990, 'original_price': 52990, 'brand': 'Lenovo',
        'stock': 20, 'rating': 4.3, 'reviews': 1230, 'sold': 2800,
        'featured': True,
        'image_url': 'https://www.lenovo.com/medias/lenovo-laptop-ideapad-slim-3-15inch-intel-gallery-1.png',
        'short_description': 'Intel Core i3 | 8GB RAM | 256GB SSD | 15.6 FHD | Win11',
        'description': 'Lenovo IdeaPad Slim 3 with Intel Core i3 processor, 8GB RAM, 256GB SSD, Windows 11.',
        'tags': 'lenovo, laptop, intel, windows, student',
    },
    {
        'name': 'Noise ColorFit Pro 4 Smartwatch',
        'category': 'Smartwatches', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 1999, 'original_price': 5999, 'brand': 'Noise',
        'stock': 200, 'rating': 4.2, 'reviews': 8900, 'sold': 28000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://www.gonoise.com/cdn/shop/products/1_pro4.png',
        'short_description': '1.85 Display | BT Calling | 100+ Sports | SpO2 | 7 Days',
        'description': 'Noise ColorFit Pro 4 with 1.85 inch display, Bluetooth calling, 100+ sports modes.',
        'tags': 'noise, smartwatch, fitness, calling',
    },
    {
        'name': "Levi's 511 Slim Fit Jeans Dark Blue",
        'category': "Men's Clothing", 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 2299, 'original_price': 3999, 'brand': "Levi's",
        'stock': 150, 'rating': 4.5, 'reviews': 4500, 'sold': 12000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://lsco.scene7.com/is/image/lsco/045111392-front-pdp',
        'short_description': 'Slim Fit | Stretch Denim | Mid Rise | 28-38 Waist',
        'description': "Levi's 511 slim fit jeans with stretch denim for comfort. Mid-rise design.",
        'tags': 'levis, jeans, denim, men, slim fit',
    },
    {
        'name': 'W Women Floral Printed Kurta',
        'category': "Women's Clothing", 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 799, 'original_price': 1599, 'brand': 'W',
        'stock': 180, 'rating': 4.4, 'reviews': 2800, 'sold': 7500,
        'featured': True,
        'image_url': 'https://assets.myntassets.com/h_1440,q_90,w_1080/v1/assets/images/16472524/2022/1/25/kurta1.jpg',
        'short_description': 'Pure Cotton | Floral Print | A-Line | XS to 3XL',
        'description': 'W women floral printed kurta made from pure cotton. A-line silhouette.',
        'tags': 'kurta, women, cotton, floral, ethnic',
    },
    {
        'name': 'Puma Men Running Shoes Flex Essential',
        'category': 'Footwear', 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 1799, 'original_price': 3499, 'brand': 'Puma',
        'stock': 100, 'rating': 4.2, 'reviews': 3200, 'sold': 8900,
        'bestseller': True,
        'image_url': 'https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_600,h_600/global/195521/01/sv01/fnd/IND/fmt/png',
        'short_description': 'Mesh Upper | Flex Grooves | Cushioned | Lightweight',
        'description': 'Puma Flex Essential running shoes with breathable mesh upper.',
        'tags': 'puma, shoes, running, sports, men',
    },
    {
        'name': 'Prestige Iris 750W Mixer Grinder 3 Jars',
        'category': 'Kitchen & Dining', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 2295, 'original_price': 4500, 'brand': 'Prestige',
        'stock': 100, 'rating': 4.4, 'reviews': 6800, 'sold': 18000,
        'bestseller': True,
        'image_url': 'https://www.prestigesmarthome.com/media/catalog/product/p/r/pr-iris-750w.jpg',
        'short_description': '750W | 3 Jars | SS Blades | 3 Speed + Pulse',
        'description': 'Prestige Iris 750W mixer grinder with 3 stainless steel jars.',
        'tags': 'prestige, mixer grinder, kitchen, appliance',
    },
    {
        'name': 'Milton Thermosteel Flip Lid Flask 500ml',
        'category': 'Kitchen & Dining', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 449, 'original_price': 895, 'brand': 'Milton',
        'stock': 500, 'rating': 4.5, 'reviews': 12000, 'sold': 45000,
        'bestseller': True,
        'image_url': 'https://www.miltonindia.com/pub/media/catalog/product/t/h/thermosteel-flip-lid-500.jpg',
        'short_description': '500ml | 24 Hours Hot/Cold | Leak Proof | BPA Free',
        'description': 'Milton Thermosteel Flip Lid Flask keeps beverages hot/cold for 24 hours.',
        'tags': 'milton, flask, thermos, bottle',
    },
    {
        'name': 'Solimo 100% Cotton Double Bedsheet',
        'category': 'Bedding', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 699, 'original_price': 1499, 'brand': 'Solimo',
        'stock': 200, 'rating': 4.3, 'reviews': 8900, 'sold': 25000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/81QpkIctqPL._SL1500_.jpg',
        'short_description': '100% Cotton | 186 TC | Double Size | 2 Pillow Covers',
        'description': 'Solimo 100% cotton double bedsheet with 186 thread count. Includes 2 pillow covers.',
        'tags': 'bedsheet, cotton, double bed, home',
    },
    {
        'name': 'Maybelline Fit Me Matte Foundation',
        'category': 'Makeup', 'parent_category': 'Beauty & Health', 'icon': 'fa-spa',
        'price': 425, 'original_price': 699, 'brand': 'Maybelline',
        'stock': 300, 'rating': 4.3, 'reviews': 8900, 'sold': 28000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://www.maybelline.in/~/media/mny/us/face-makeup/foundation/fit-me-matte-poreless-foundation/fit-me-matte-foundation.jpg',
        'short_description': '30ml | Matte Finish | Pore-Minimizing | SPF 22',
        'description': 'Maybelline Fit Me Matte+Poreless Foundation with SPF 22, blurs pores.',
        'tags': 'maybelline, foundation, makeup, matte',
    },
    {
        'name': 'Himalaya Purifying Neem Face Wash 150ml',
        'category': 'Skincare', 'parent_category': 'Beauty & Health', 'icon': 'fa-spa',
        'price': 105, 'original_price': 175, 'brand': 'Himalaya',
        'stock': 800, 'rating': 4.4, 'reviews': 25000, 'sold': 95000,
        'bestseller': True,
        'image_url': 'https://www.himalayawellness.in/cdn/shop/products/PurifyingNeemFaceWash150ml.jpg',
        'short_description': '150ml | Neem + Turmeric | Anti-Bacterial | Acne Control',
        'description': 'Himalaya Purifying Neem Face Wash with neem and turmeric.',
        'tags': 'himalaya, face wash, neem, skincare',
    },
    {
        'name': 'Strauss Yoga Mat 6mm Anti-Slip',
        'category': 'Yoga', 'parent_category': 'Sports & Outdoors', 'icon': 'fa-football-ball',
        'price': 449, 'original_price': 999, 'brand': 'Strauss',
        'stock': 300, 'rating': 4.3, 'reviews': 5600, 'sold': 18000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/61T5ZqcmqhL._SL1500_.jpg',
        'short_description': '6mm Thick | Anti-Slip | NBR Foam | Carrying Strap',
        'description': 'Strauss 6mm thick yoga mat made from NBR foam. Anti-slip texture.',
        'tags': 'yoga mat, exercise, fitness, yoga',
    },
    {
        'name': 'Atomic Habits by James Clear',
        'category': 'Non-Fiction', 'parent_category': 'Books & Stationery', 'icon': 'fa-book',
        'price': 299, 'original_price': 599, 'brand': 'Penguin',
        'stock': 500, 'rating': 4.8, 'reviews': 15000, 'sold': 55000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/81wgcld4wxL._AC_UF1000,1000_QL80_.jpg',
        'short_description': 'Paperback | 320 Pages | Self Help | Bestseller',
        'description': 'Atomic Habits by James Clear — practical strategies to build good habits.',
        'tags': 'atomic habits, self help, book',
    },
    {
        'name': 'LEGO Classic Creative Bricks 484 Pieces',
        'category': 'Building Blocks', 'parent_category': 'Toys & Games', 'icon': 'fa-gamepad',
        'price': 1499, 'original_price': 2499, 'brand': 'LEGO',
        'stock': 100, 'rating': 4.8, 'reviews': 2800, 'sold': 7500,
        'featured': True,
        'image_url': 'https://www.lego.com/cdn/cs/set/assets/blt81a5bfa4e8d2f4f5/10696.jpg',
        'short_description': '484 Pieces | Age 4+ | Creative Play | STEM',
        'description': 'LEGO Classic Creative Bricks set with 484 pieces. Open-ended building.',
        'tags': 'lego, building blocks, toys, kids',
    },
    {
        'name': 'Aashirvaad Whole Wheat Atta 5kg',
        'category': 'Instant Food', 'parent_category': 'Grocery & Food', 'icon': 'fa-shopping-basket',
        'price': 245, 'original_price': 290, 'brand': 'Aashirvaad',
        'stock': 500, 'rating': 4.5, 'reviews': 22000, 'sold': 95000,
        'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/71xvBCbMZcL._SL1500_.jpg',
        'short_description': '5kg | 100% Whole Wheat | MP Sharbati Wheat',
        'description': 'Aashirvaad Whole Wheat Atta made from superior MP Sharbati wheat.',
        'tags': 'atta, wheat flour, grocery, roti',
    },
    {
        'name': 'Haldirams Bhujia Sev 1kg',
        'category': 'Snacks', 'parent_category': 'Grocery & Food', 'icon': 'fa-shopping-basket',
        'price': 299, 'original_price': 380, 'brand': 'Haldirams',
        'stock': 800, 'rating': 4.6, 'reviews': 18000, 'sold': 75000,
        'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/81MJKXzMiLL._SL1500_.jpg',
        'short_description': '1kg | Crispy | Traditional Recipe | No Preservatives',
        'description': 'Haldirams Bhujia Sev 1kg pack. Crispy and flavorful namkeen snack.',
        'tags': 'haldirams, bhujia, snacks, namkeen',
    },
    {
        'name': 'Vega Crux Full Face Helmet ISI',
        'category': 'Helmets', 'parent_category': 'Automotive', 'icon': 'fa-car',
        'price': 999, 'original_price': 1799, 'brand': 'Vega',
        'stock': 150, 'rating': 4.3, 'reviews': 5600, 'sold': 18000,
        'featured': True, 'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/61c-QEiTGnL._AC_UL1200_.jpg',
        'short_description': 'Full Face | ISI Certified | ABS Shell | M/L/XL',
        'description': 'Vega Crux full face helmet with ISI certification, ABS thermoplastic shell.',
        'tags': 'helmet, vega, bike, safety',
    },
    {
        'name': 'Pedigree Adult Dog Food Chicken 3kg',
        'category': 'Dog Food', 'parent_category': 'Pet Supplies', 'icon': 'fa-paw',
        'price': 699, 'original_price': 999, 'brand': 'Pedigree',
        'stock': 200, 'rating': 4.5, 'reviews': 4500, 'sold': 15000,
        'bestseller': True,
        'image_url': 'https://m.media-amazon.com/images/I/81o3tFtbVQL._AC_UL1500_.jpg',
        'short_description': '3kg | Chicken & Vegetables | Adult Dogs | Omega 6',
        'description': 'Pedigree Adult Dog Food with chicken and vegetables. Omega 6 for healthy coat.',
        'tags': 'pedigree, dog food, pet, chicken',
    },
]

print(f"\nAdding {len(products)} products...\n")
for p in products:
    add_product(p)

total = Product.objects.filter(is_active=True).count()
print(f"\n{'='*60}")
print(f"  Done! Total Products: {total}")
print(f"{'='*60}")
print(f"  Website: http://127.0.0.1:8000/")
print(f"  Admin:   http://127.0.0.1:8000/admin/")
print(f"{'='*60}\n")