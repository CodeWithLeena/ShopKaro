#!/usr/bin/env python
"""
ShopKaro - Auto Product Seeder
Automatically adds 50+ products across all categories with images from internet
Run: python3 seed_products.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopkaro.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from store.models import Category, Product, ProductImage, SellerProfile
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request

print("\n" + "="*60)
print("  🛒 ShopKaro - Auto Product Seeder")
print("="*60)

# Get or create seller
try:
    seller = SellerProfile.objects.filter(is_approved=True).first()
    if not seller:
        user = User.objects.filter(is_superuser=True).first()
        seller = SellerProfile.objects.create(
            user=user,
            shop_name='ShopKaro Official',
            is_approved=True,
            rating=4.5
        )
except:
    seller = None

def get_or_create_category(name, parent_name=None, icon='fa-tag'):
    parent = None
    if parent_name:
        parent, _ = Category.objects.get_or_create(
            name=parent_name,
            defaults={'icon': icon}
        )
    cat, _ = Category.objects.get_or_create(
        name=name,
        defaults={'parent': parent, 'icon': icon}
    )
    return cat

def add_product(data):
    cat = get_or_create_category(data['category'], data.get('parent_category'), data.get('icon', 'fa-tag'))
    
    product, created = Product.objects.get_or_create(
        name=data['name'],
        defaults={
            'category': cat,
            'seller': seller,
            'description': data['description'],
            'short_description': data.get('short_description', ''),
            'price': data['price'],
            'original_price': data.get('original_price', None),
            'stock': data.get('stock', 50),
            'brand': data.get('brand', ''),
            'rating': data.get('rating', 4.0),
            'total_reviews': data.get('reviews', 100),
            'total_sold': data.get('sold', 500),
            'is_active': True,
            'is_featured': data.get('featured', False),
            'is_bestseller': data.get('bestseller', False),
            'tags': data.get('tags', ''),
            'condition': 'new',
        }
    )
    
    if created:
        print(f"  ✅ Added: {data['name']}")
    else:
        print(f"  ℹ️  Exists: {data['name']}")
    
    return product

# ============================================================
# ALL PRODUCTS DATA
# ============================================================

products = [

    # =================== ELECTRONICS ===================
    {
        'name': 'Samsung Galaxy S23 Ultra 5G',
        'category': 'Mobile Phones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 99999, 'original_price': 124999,
        'brand': 'Samsung', 'stock': 30, 'rating': 4.7, 'reviews': 3420, 'sold': 8900,
        'featured': True, 'bestseller': True,
        'short_description': '200MP Camera | 12GB RAM | 256GB | S-Pen | 5000mAh Battery',
        'description': 'Samsung Galaxy S23 Ultra 5G with 200MP main camera, built-in S-Pen, 12GB RAM, 256GB storage. Features Dynamic AMOLED 2X display with 120Hz refresh rate. Snapdragon 8 Gen 2 processor. 5000mAh battery with 45W fast charging.',
        'tags': 'samsung, smartphone, 5g, s23, android, flagship',
    },
    {
        'name': 'iPhone 14 128GB Blue',
        'category': 'Mobile Phones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 69999, 'original_price': 79900,
        'brand': 'Apple', 'stock': 25, 'rating': 4.8, 'reviews': 5621, 'sold': 12000,
        'featured': True, 'bestseller': True,
        'short_description': 'A15 Bionic | 12MP Dual Camera | 5G | Face ID | iOS 16',
        'description': 'Apple iPhone 14 with A15 Bionic chip, 12MP dual camera system with photonic engine, 5G connectivity, Face ID, and all-day battery life. Available in 128GB storage.',
        'tags': 'iphone, apple, smartphone, ios, 5g',
    },
    {
        'name': 'OnePlus Nord CE 3 Lite 5G',
        'category': 'Mobile Phones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 19999, 'original_price': 25999,
        'brand': 'OnePlus', 'stock': 80, 'rating': 4.2, 'reviews': 2100, 'sold': 6500,
        'featured': True,
        'short_description': '108MP Camera | 8GB RAM | 128GB | 67W Charging | 5000mAh',
        'description': 'OnePlus Nord CE 3 Lite 5G with 108MP main camera, 8GB RAM, 128GB storage, 67W SUPERVOOC fast charging, and 5000mAh battery. Snapdragon 695 5G processor.',
        'tags': 'oneplus, nord, 5g, smartphone, android',
    },
    {
        'name': 'boAt Airdopes 141 TWS Earbuds',
        'category': 'Headphones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 999, 'original_price': 3990,
        'brand': 'boAt', 'stock': 500, 'rating': 4.1, 'reviews': 25000, 'sold': 85000,
        'bestseller': True,
        'short_description': '42 Hours Playback | ENx Tech | BEAST Mode | IPX4',
        'description': 'boAt Airdopes 141 TWS earbuds with 42 hours total playback, ENx technology for clear calls, BEAST mode for low latency gaming, IPX4 water resistance.',
        'tags': 'earbuds, tws, wireless, boat, bluetooth',
    },
    {
        'name': 'Sony WH-1000XM5 Noise Cancelling Headphones',
        'category': 'Headphones', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 24990, 'original_price': 34990,
        'brand': 'Sony', 'stock': 40, 'rating': 4.8, 'reviews': 1890, 'sold': 4200,
        'featured': True,
        'short_description': 'Industry Leading ANC | 30 Hours Battery | LDAC | Multipoint',
        'description': 'Sony WH-1000XM5 with industry-leading noise cancellation, 30-hour battery life, LDAC Hi-Res Audio, multipoint connection, and speak-to-chat feature.',
        'tags': 'sony, headphones, noise cancelling, wireless, premium',
    },
    {
        'name': 'Lenovo IdeaPad Slim 3 Laptop',
        'category': 'Laptops', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 37990, 'original_price': 52990,
        'brand': 'Lenovo', 'stock': 20, 'rating': 4.3, 'reviews': 1230, 'sold': 2800,
        'featured': True,
        'short_description': 'Intel Core i3 | 8GB RAM | 256GB SSD | 15.6" FHD | Win11',
        'description': 'Lenovo IdeaPad Slim 3 with Intel Core i3-1215U processor, 8GB DDR4 RAM, 256GB SSD, 15.6-inch Full HD display, Windows 11 Home. Thin and light design perfect for students.',
        'tags': 'lenovo, laptop, student, intel, windows',
    },
    {
        'name': 'Samsung 55" 4K Smart TV',
        'category': 'TVs', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 44990, 'original_price': 74900,
        'brand': 'Samsung', 'stock': 15, 'rating': 4.5, 'reviews': 890, 'sold': 1500,
        'featured': True,
        'short_description': '55" Crystal 4K | HDR | Tizen OS | Voice Control | 3 HDMI',
        'description': 'Samsung 55-inch Crystal 4K Smart TV with HDR, Tizen OS, voice control, 3 HDMI ports, 2 USB ports, and built-in WiFi. Crystal Processor 4K for detailed picture quality.',
        'tags': 'samsung, tv, smart tv, 4k, television',
    },
    {
        'name': 'Apple Watch Series 8 GPS 41mm',
        'category': 'Smartwatches', 'parent_category': 'Electronics', 'icon': 'fa-laptop',
        'price': 38900, 'original_price': 45900,
        'brand': 'Apple', 'stock': 30, 'rating': 4.7, 'reviews': 2100, 'sold': 5600,
        'featured': True,
        'short_description': 'Always-On Retina Display | Heart Rate | Blood Oxygen | GPS',
        'description': 'Apple Watch Series 8 with always-on Retina display, advanced health sensors including heart rate, blood oxygen, ECG. Crash detection, GPS tracking, and 18-hour battery life.',
        'tags': 'apple watch, smartwatch, fitness, health, ios',
    },

    # =================== FASHION ===================
    {
        'name': 'Allen Solly Men Slim Fit Formal Shirt',
        'category': "Men's Clothing", 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 899, 'original_price': 1799,
        'brand': 'Allen Solly', 'stock': 200, 'rating': 4.3, 'reviews': 3400, 'sold': 9800,
        'featured': True, 'bestseller': True,
        'short_description': 'Slim Fit | Cotton Blend | Full Sleeve | Formal | S to 3XL',
        'description': 'Allen Solly slim fit formal shirt made from premium cotton blend fabric. Full sleeve with button cuffs. Suitable for office and formal occasions. Machine washable.',
        'tags': 'shirt, formal, men, allen solly, office wear',
    },
    {
        'name': 'Levi\'s 511 Slim Fit Jeans',
        'category': "Men's Clothing", 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 2299, 'original_price': 3999,
        'brand': "Levi's", 'stock': 150, 'rating': 4.5, 'reviews': 4500, 'sold': 12000,
        'featured': True, 'bestseller': True,
        'short_description': 'Slim Fit | Stretch Denim | Mid Rise | 28-38 Waist',
        'description': "Levi's 511 slim fit jeans with stretch denim for comfort. Mid-rise design, zip fly, 5-pocket styling. The perfect everyday jean for a modern slim silhouette.",
        'tags': 'levis, jeans, denim, men, slim fit',
    },
    {
        'name': 'W Women Floral Printed Kurta',
        'category': "Women's Clothing", 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 799, 'original_price': 1599,
        'brand': 'W', 'stock': 180, 'rating': 4.4, 'reviews': 2800, 'sold': 7500,
        'featured': True,
        'short_description': 'Pure Cotton | Floral Print | A-Line | XS to 3XL | Casual',
        'description': 'W women floral printed kurta made from pure cotton. A-line silhouette with 3/4 sleeves. Beautiful floral print perfect for casual and festive occasions.',
        'tags': 'kurta, women, cotton, floral, ethnic',
    },
    {
        'name': 'Puma Men Running Shoes Flex Essential',
        'category': 'Footwear', 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 1799, 'original_price': 3499,
        'brand': 'Puma', 'stock': 100, 'rating': 4.2, 'reviews': 3200, 'sold': 8900,
        'bestseller': True,
        'short_description': 'Mesh Upper | Flex Grooves | Cushioned | UK 6-11 | Lightweight',
        'description': 'Puma Flex Essential running shoes with breathable mesh upper, flex grooves for natural movement, and cushioned midsole. Lightweight and durable for everyday running.',
        'tags': 'puma, shoes, running, sports, men',
    },
    {
        'name': 'H&M Women Oversized T-Shirt',
        'category': "Women's Clothing", 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 499, 'original_price': 999,
        'brand': 'H&M', 'stock': 300, 'rating': 4.1, 'reviews': 1800, 'sold': 5600,
        'featured': True,
        'short_description': 'Oversized Fit | 100% Cotton | Round Neck | XS to XXL',
        'description': 'H&M oversized t-shirt in 100% soft cotton. Round neck with dropped shoulders for a relaxed fit. Perfect for casual everyday wear.',
        'tags': 'hm, tshirt, women, oversized, casual',
    },
    {
        'name': 'Fastrack Analog Watch for Men',
        'category': 'Accessories', 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 1295, 'original_price': 2495,
        'brand': 'Fastrack', 'stock': 120, 'rating': 4.3, 'reviews': 4200, 'sold': 11000,
        'bestseller': True,
        'short_description': 'Analog | Day-Date | Water Resistant | Stainless Steel | Quartz',
        'description': 'Fastrack analog watch with day-date display, water-resistant design, stainless steel case and bracelet. Quartz movement for accurate timekeeping.',
        'tags': 'fastrack, watch, men, analog, accessories',
    },
    {
        'name': 'Baggit Women Tote Handbag',
        'category': 'Bags & Wallets', 'parent_category': 'Fashion', 'icon': 'fa-tshirt',
        'price': 1299, 'original_price': 2599,
        'brand': 'Baggit', 'stock': 80, 'rating': 4.2, 'reviews': 1500, 'sold': 3800,
        'featured': True,
        'short_description': 'PU Leather | Multiple Compartments | Zipper | Shoulder Bag',
        'description': 'Baggit women tote handbag in premium PU leather with multiple compartments, inner zipper pocket, and adjustable shoulder strap. Spacious and stylish for everyday use.',
        'tags': 'baggit, handbag, women, tote, bag',
    },

    # =================== HOME & LIVING ===================
    {
        'name': 'Prestige Iris 750W Mixer Grinder',
        'category': 'Kitchen & Dining', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 2295, 'original_price': 4500,
        'brand': 'Prestige', 'stock': 100, 'rating': 4.4, 'reviews': 6800, 'sold': 18000,
        'bestseller': True,
        'short_description': '750W | 3 Jars | SS Blades | Anti-Slip Feet | 3 Speed + Pulse',
        'description': 'Prestige Iris 750W mixer grinder with 3 stainless steel jars, sharp SS blades, 3 speed control + pulse function, anti-slip feet. Suitable for grinding, mixing, and juicing.',
        'tags': 'prestige, mixer grinder, kitchen, appliance, grinder',
    },
    {
        'name': 'Milton Thermosteel Flip Lid Flask 500ml',
        'category': 'Kitchen & Dining', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 449, 'original_price': 895,
        'brand': 'Milton', 'stock': 500, 'rating': 4.5, 'reviews': 12000, 'sold': 45000,
        'bestseller': True,
        'short_description': '500ml | 24 Hours Hot/Cold | SS Inner | Leak Proof | BPA Free',
        'description': 'Milton Thermosteel Flip Lid Flask 500ml keeps beverages hot for 24 hours and cold for 24 hours. Stainless steel inner body, leak-proof flip lid, BPA-free.',
        'tags': 'milton, flask, thermos, hot cold, bottle',
    },
    {
        'name': 'Solimo 100% Cotton Double Bedsheet',
        'category': 'Bedding', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 699, 'original_price': 1499,
        'brand': 'Solimo', 'stock': 200, 'rating': 4.3, 'reviews': 8900, 'sold': 25000,
        'featured': True, 'bestseller': True,
        'short_description': '100% Cotton | 186 TC | Double Size | 2 Pillow Covers | Washable',
        'description': 'Solimo 100% cotton double bedsheet with 186 thread count for softness and durability. Includes 2 matching pillow covers. Machine washable, colorfast fabric.',
        'tags': 'bedsheet, cotton, double bed, solimo, home',
    },
    {
        'name': 'Philips LED Bulb 9W B22 Pack of 4',
        'category': 'Lighting', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 299, 'original_price': 599,
        'brand': 'Philips', 'stock': 1000, 'rating': 4.4, 'reviews': 15000, 'sold': 60000,
        'bestseller': True,
        'short_description': '9W | 900 Lumens | Cool White | B22 | 15000 Hours Life',
        'description': 'Philips 9W LED bulbs with B22 base, 900 lumens brightness, cool white light. Energy efficient, saving up to 88% compared to incandescent. 15000 hours lifespan.',
        'tags': 'philips, led bulb, light, energy saving, home',
    },
    {
        'name': 'Godrej Interio Slimline Wardrobe',
        'category': 'Furniture', 'parent_category': 'Home & Living', 'icon': 'fa-home',
        'price': 15999, 'original_price': 22000,
        'brand': 'Godrej', 'stock': 10, 'rating': 4.3, 'reviews': 450, 'sold': 890,
        'featured': True,
        'short_description': '2 Door | Engineered Wood | Mirror | 5 Shelves | Easy Assembly',
        'description': 'Godrej Interio 2-door slimline wardrobe with full-length mirror, 5 shelves and hanging space. Made from engineered wood. Easy DIY assembly. Space-saving design.',
        'tags': 'wardrobe, godrej, furniture, bedroom, storage',
    },

    # =================== BEAUTY & HEALTH ===================
    {
        'name': 'Maybelline Fit Me Matte+Poreless Foundation',
        'category': 'Makeup', 'parent_category': 'Beauty & Health', 'icon': 'fa-spa',
        'price': 425, 'original_price': 699,
        'brand': 'Maybelline', 'stock': 300, 'rating': 4.3, 'reviews': 8900, 'sold': 28000,
        'featured': True, 'bestseller': True,
        'short_description': '30ml | Matte Finish | Pore-Minimizing | SPF 22 | 16 Shades',
        'description': 'Maybelline Fit Me Matte+Poreless Foundation with SPF 22, blurs pores, controls shine for a natural matte finish. Available in 16 shades for Indian skin tones.',
        'tags': 'maybelline, foundation, makeup, matte, beauty',
    },
    {
        'name': "L'Oreal Paris Hair Fall Repair Shampoo 650ml",
        'category': 'Haircare', 'parent_category': 'Beauty & Health', 'icon': 'fa-spa',
        'price': 449, 'original_price': 699,
        'brand': "L'Oreal", 'stock': 400, 'rating': 4.2, 'reviews': 6700, 'sold': 22000,
        'bestseller': True,
        'short_description': '650ml | Arginine + Wheat Protein | Anti Hair Fall | All Hair Types',
        'description': "L'Oreal Paris Hair Fall Repair Shampoo with Arginine and Wheat Protein complex. Reduces hair fall due to breakage by up to 97%. Suitable for all hair types.",
        'tags': 'loreal, shampoo, haircare, anti hairfall, hair',
    },
    {
        'name': 'Himalaya Purifying Neem Face Wash 150ml',
        'category': 'Skincare', 'parent_category': 'Beauty & Health', 'icon': 'fa-spa',
        'price': 105, 'original_price': 175,
        'brand': 'Himalaya', 'stock': 800, 'rating': 4.4, 'reviews': 25000, 'sold': 95000,
        'bestseller': True,
        'short_description': '150ml | Neem + Turmeric | Anti-Bacterial | Acne Control | Gentle',
        'description': 'Himalaya Purifying Neem Face Wash with neem and turmeric. Anti-bacterial properties help control acne. Gentle enough for daily use. Suitable for oily and combination skin.',
        'tags': 'himalaya, face wash, neem, skincare, acne',
    },
    {
        'name': 'Omron HEM-7120 Blood Pressure Monitor',
        'category': 'Health Devices', 'parent_category': 'Beauty & Health', 'icon': 'fa-spa',
        'price': 1799, 'original_price': 2999,
        'brand': 'Omron', 'stock': 150, 'rating': 4.5, 'reviews': 3400, 'sold': 8900,
        'featured': True,
        'short_description': 'Automatic | Upper Arm | 60 Memory | Irregular Heartbeat | Cuff',
        'description': 'Omron HEM-7120 automatic blood pressure monitor for upper arm. Stores 60 readings in memory, detects irregular heartbeat, easy one-touch operation. Includes cuff and batteries.',
        'tags': 'omron, bp monitor, health, blood pressure, medical',
    },

    # =================== SPORTS ===================
    {
        'name': 'Cosco Striker Football Size 5',
        'category': 'Football', 'parent_category': 'Sports & Outdoors', 'icon': 'fa-football-ball',
        'price': 399, 'original_price': 799,
        'brand': 'Cosco', 'stock': 200, 'rating': 4.2, 'reviews': 2800, 'sold': 8500,
        'bestseller': True,
        'short_description': 'Size 5 | 32 Panel | PU Material | Match Ball | All Surfaces',
        'description': 'Cosco Striker football size 5 with 32-panel design, PU material outer layer for durability. Suitable for all playing surfaces. Ideal for practice and matches.',
        'tags': 'football, cosco, sports, soccer, outdoor',
    },
    {
        'name': 'Strauss Yoga Mat 6mm Anti-Slip',
        'category': 'Yoga', 'parent_category': 'Sports & Outdoors', 'icon': 'fa-football-ball',
        'price': 449, 'original_price': 999,
        'brand': 'Strauss', 'stock': 300, 'rating': 4.3, 'reviews': 5600, 'sold': 18000,
        'featured': True, 'bestseller': True,
        'short_description': '6mm Thick | Anti-Slip | NBR Foam | Carrying Strap | 183x61cm',
        'description': 'Strauss 6mm thick yoga mat made from NBR foam. Anti-slip texture on both sides for stability. Includes carrying strap. Size 183x61cm. Ideal for yoga, pilates, and exercise.',
        'tags': 'yoga mat, strauss, exercise, fitness, yoga',
    },
    {
        'name': 'Decathlon Domyos Dumbbell Set 10kg',
        'category': 'Gym & Fitness', 'parent_category': 'Sports & Outdoors', 'icon': 'fa-football-ball',
        'price': 1299, 'original_price': 2000,
        'brand': 'Decathlon', 'stock': 80, 'rating': 4.4, 'reviews': 1800, 'sold': 4500,
        'featured': True,
        'short_description': '2x5kg | Cast Iron | Rubber Coating | Anti-Slip Grip | Home Gym',
        'description': 'Decathlon Domyos dumbbell set with two 5kg dumbbells. Cast iron with rubber coating to protect floors. Anti-slip textured grip for secure hold. Perfect for home workouts.',
        'tags': 'dumbbell, gym, fitness, weights, exercise',
    },

    # =================== BOOKS ===================
    {
        'name': 'Atomic Habits by James Clear',
        'category': 'Non-Fiction', 'parent_category': 'Books & Stationery', 'icon': 'fa-book',
        'price': 299, 'original_price': 599,
        'brand': 'Penguin', 'stock': 500, 'rating': 4.8, 'reviews': 15000, 'sold': 55000,
        'featured': True, 'bestseller': True,
        'short_description': 'Paperback | 320 Pages | Self Help | English | Bestseller',
        'description': 'Atomic Habits by James Clear — the #1 bestselling book on habit formation. Learn how tiny changes lead to remarkable results. Practical strategies to build good habits and break bad ones.',
        'tags': 'atomic habits, james clear, self help, book, habits',
    },
    {
        'name': 'Rich Dad Poor Dad by Robert Kiyosaki',
        'category': 'Non-Fiction', 'parent_category': 'Books & Stationery', 'icon': 'fa-book',
        'price': 249, 'original_price': 450,
        'brand': 'Manjul Publishing', 'stock': 400, 'rating': 4.7, 'reviews': 18000, 'sold': 65000,
        'bestseller': True,
        'short_description': 'Paperback | 336 Pages | Finance | English | All Time Bestseller',
        'description': 'Rich Dad Poor Dad by Robert Kiyosaki — the world\'s #1 personal finance book. Learn the difference between assets and liabilities, and how to make money work for you.',
        'tags': 'rich dad poor dad, robert kiyosaki, finance, book, money',
    },
    {
        'name': 'Classmate Pulse Notebook Pack of 6',
        'category': 'Notebooks', 'parent_category': 'Books & Stationery', 'icon': 'fa-book',
        'price': 180, 'original_price': 270,
        'brand': 'Classmate', 'stock': 1000, 'rating': 4.3, 'reviews': 8900, 'sold': 35000,
        'bestseller': True,
        'short_description': 'A5 | 172 Pages | Single Line | Hard Cover | Pack of 6',
        'description': 'Classmate Pulse A5 notebooks pack of 6, single line ruling, 172 pages each. Hard cover with vibrant design. Smooth paper quality for comfortable writing.',
        'tags': 'classmate, notebook, stationery, school, writing',
    },

    # =================== TOYS & GAMES ===================
    {
        'name': 'LEGO Classic Creative Bricks Set',
        'category': 'Building Blocks', 'parent_category': 'Toys & Games', 'icon': 'fa-gamepad',
        'price': 1499, 'original_price': 2499,
        'brand': 'LEGO', 'stock': 100, 'rating': 4.8, 'reviews': 2800, 'sold': 7500,
        'featured': True,
        'short_description': '484 Pieces | Age 4+ | Creative Play | Classic Colors | STEM',
        'description': 'LEGO Classic Creative Bricks set with 484 pieces in classic colors. Open-ended building for unlimited creativity. Suitable for ages 4 and above. Compatible with all LEGO sets.',
        'tags': 'lego, building blocks, toys, kids, creative',
    },
    {
        'name': 'Funskool Monopoly Board Game',
        'category': 'Board Games', 'parent_category': 'Toys & Games', 'icon': 'fa-gamepad',
        'price': 699, 'original_price': 1299,
        'brand': 'Funskool', 'stock': 150, 'rating': 4.5, 'reviews': 6700, 'sold': 22000,
        'bestseller': True,
        'short_description': '2-6 Players | Age 8+ | Classic Edition | Property Trading | Family',
        'description': 'Funskool Monopoly Classic board game for 2-6 players. The classic property trading game that everyone loves. Includes game board, dice, tokens, property cards, and play money.',
        'tags': 'monopoly, board game, family, funskool, game',
    },
    {
        'name': 'Hot Wheels 20 Car Gift Pack',
        'category': 'Action Figures', 'parent_category': 'Toys & Games', 'icon': 'fa-gamepad',
        'price': 799, 'original_price': 1399,
        'brand': 'Hot Wheels', 'stock': 200, 'rating': 4.6, 'reviews': 4500, 'sold': 15000,
        'featured': True, 'bestseller': True,
        'short_description': 'Pack of 20 | Die-Cast Metal | Age 3+ | Random Models | Collectible',
        'description': 'Hot Wheels 20 car gift pack with die-cast metal cars in random models. Suitable for ages 3 and above. Perfect birthday gift for car-loving kids. Collectible and durable.',
        'tags': 'hot wheels, cars, toys, kids, die cast',
    },

    # =================== GROCERY ===================
    {
        'name': 'Tata Salt Lite Low Sodium 1kg',
        'category': 'Dry Fruits', 'parent_category': 'Grocery & Food', 'icon': 'fa-shopping-basket',
        'price': 28, 'original_price': 35,
        'brand': 'Tata', 'stock': 2000, 'rating': 4.4, 'reviews': 12000, 'sold': 80000,
        'bestseller': True,
        'short_description': '1kg | Low Sodium | Iodized | Health Salt | Tata Quality',
        'description': 'Tata Salt Lite with 15% less sodium than regular salt. Iodized for essential nutrients. Ideal for people watching sodium intake. Trusted Tata quality.',
        'tags': 'tata salt, salt, grocery, low sodium, kitchen',
    },
    {
        'name': 'Aashirvaad Atta Whole Wheat 5kg',
        'category': 'Instant Food', 'parent_category': 'Grocery & Food', 'icon': 'fa-shopping-basket',
        'price': 245, 'original_price': 290,
        'brand': 'Aashirvaad', 'stock': 500, 'rating': 4.5, 'reviews': 22000, 'sold': 95000,
        'bestseller': True,
        'short_description': '5kg | 100% Whole Wheat | MP Sharbati Wheat | Superior Roti',
        'description': 'Aashirvaad Whole Wheat Atta made from superior MP Sharbati wheat. 100% whole wheat with natural fiber. Makes soft rotis that stay soft for longer. No additives or preservatives.',
        'tags': 'aashirvaad, atta, wheat flour, grocery, roti',
    },
    {
        'name': 'Haldirams Bhujia Sev 1kg',
        'category': 'Snacks', 'parent_category': 'Grocery & Food', 'icon': 'fa-shopping-basket',
        'price': 299, 'original_price': 380,
        'brand': 'Haldirams', 'stock': 800, 'rating': 4.6, 'reviews': 18000, 'sold': 75000,
        'bestseller': True,
        'short_description': '1kg | Crispy | Traditional Recipe | No Preservatives | Namkeen',
        'description': 'Haldirams Bhujia Sev 1kg pack made from traditional recipe. Crispy and flavorful namkeen snack. Made from moth beans and spices. No artificial preservatives.',
        'tags': 'haldirams, bhujia, snacks, namkeen, grocery',
    },
    {
        'name': 'Bru Instant Coffee 200g',
        'category': 'Beverages', 'parent_category': 'Grocery & Food', 'icon': 'fa-shopping-basket',
        'price': 249, 'original_price': 310,
        'brand': 'Bru', 'stock': 600, 'rating': 4.4, 'reviews': 14000, 'sold': 58000,
        'bestseller': True,
        'short_description': '200g | Instant Coffee | Chicory Blend | Rich Aroma | No. 1 Brand',
        'description': "Bru Instant Coffee 200g with chicory blend for rich aroma and taste. India's #1 coffee brand. Just add hot water or milk for a perfect cup. Available in convenient jar.",
        'tags': 'bru, coffee, instant coffee, beverage, drink',
    },

    # =================== AUTOMOTIVE ===================
    {
        'name': 'Vega Crux Helmet ISI Certified',
        'category': 'Helmets', 'parent_category': 'Automotive', 'icon': 'fa-car',
        'price': 999, 'original_price': 1799,
        'brand': 'Vega', 'stock': 150, 'rating': 4.3, 'reviews': 5600, 'sold': 18000,
        'featured': True, 'bestseller': True,
        'short_description': 'Full Face | ISI Certified | ABS Shell | Quick Release | M/L/XL',
        'description': 'Vega Crux full face helmet with ISI certification, ABS thermoplastic shell, quick release buckle, interior padding, and ventilation system. Sizes M, L, XL available.',
        'tags': 'helmet, vega, bike, safety, isi certified',
    },
    {
        'name': '3M Car Cleaning Kit 9-in-1',
        'category': 'Car Care', 'parent_category': 'Automotive', 'icon': 'fa-car',
        'price': 699, 'original_price': 1299,
        'brand': '3M', 'stock': 200, 'rating': 4.4, 'reviews': 3200, 'sold': 9800,
        'featured': True,
        'short_description': '9 Products | Dashboard Polish | Glass Cleaner | Tyre Shine | Kit',
        'description': '3M Car Cleaning Kit with 9 essential products including dashboard polish, glass cleaner, tyre shine, upholstery cleaner, and microfiber cloth. Complete car care solution.',
        'tags': '3m, car care, cleaning, automotive, polish',
    },

    # =================== JEWELLERY ===================
    {
        'name': 'Malabar Gold 22K Gold Stud Earrings',
        'category': 'Earrings', 'parent_category': 'Jewellery', 'icon': 'fa-gem',
        'price': 8500, 'original_price': 9200,
        'brand': 'Malabar Gold', 'stock': 20, 'rating': 4.7, 'reviews': 890, 'sold': 1800,
        'featured': True,
        'short_description': '22K Gold | 1.2g | BIS Hallmarked | Certificate | Free Shipping',
        'description': 'Malabar Gold 22K gold stud earrings with BIS hallmark certification. Weight 1.2g. Beautiful floral design. Comes with certificate of authenticity. Free insured shipping.',
        'tags': 'gold earrings, malabar gold, jewellery, 22k, earrings',
    },
    {
        'name': 'Voylla Silver Oxidized Bangles Set of 4',
        'category': 'Bangles', 'parent_category': 'Jewellery', 'icon': 'fa-gem',
        'price': 449, 'original_price': 999,
        'brand': 'Voylla', 'stock': 100, 'rating': 4.3, 'reviews': 2400, 'sold': 6500,
        'featured': True,
        'short_description': 'Set of 4 | Silver Oxidized | Ethnic | Adjustable | Gift Box',
        'description': 'Voylla silver oxidized bangles set of 4 with intricate ethnic design. Adjustable size fits most wrists. Comes in an elegant gift box. Perfect for festivals and weddings.',
        'tags': 'bangles, silver, oxidized, jewellery, ethnic',
    },

    # =================== PET SUPPLIES ===================
    {
        'name': 'Pedigree Adult Dog Food Chicken 3kg',
        'category': 'Dog Food', 'parent_category': 'Pet Supplies', 'icon': 'fa-paw',
        'price': 699, 'original_price': 999,
        'brand': 'Pedigree', 'stock': 200, 'rating': 4.5, 'reviews': 4500, 'sold': 15000,
        'bestseller': True,
        'short_description': '3kg | Chicken & Vegetables | Adult Dogs | Omega 6 | Vet Recommended',
        'description': 'Pedigree Adult Dog Food with chicken and vegetables. Contains Omega 6 for healthy skin and coat. Calcium and phosphorus for strong teeth and bones. Vet recommended nutrition.',
        'tags': 'pedigree, dog food, pet, adult dog, chicken',
    },
    {
        'name': 'Whiskas Adult Cat Food Ocean Fish 1.2kg',
        'category': 'Cat Food', 'parent_category': 'Pet Supplies', 'icon': 'fa-paw',
        'price': 399, 'original_price': 599,
        'brand': 'Whiskas', 'stock': 300, 'rating': 4.4, 'reviews': 3200, 'sold': 11000,
        'bestseller': True,
        'short_description': '1.2kg | Ocean Fish | Adult Cats | Taurine | Complete Nutrition',
        'description': 'Whiskas Adult Cat Food with ocean fish flavor. Contains taurine for healthy heart and vision. Complete and balanced nutrition for adult cats aged 1-7 years.',
        'tags': 'whiskas, cat food, pet, adult cat, fish',
    },
]

# ============================================================
# ADD ALL PRODUCTS
# ============================================================

print(f"\nAdding {len(products)} products...\n")
for p in products:
    add_product(p)

total = Product.objects.filter(is_active=True).count()
print(f"\n{'='*60}")
print(f"  ✅ Done! Total Products in Database: {total}")
print(f"{'='*60}")
print(f"\n  🌐 Website: http://127.0.0.1:8000/")
print(f"  🔐 Admin:   http://127.0.0.1:8000/admin/")
print(f"{'='*60}\n")