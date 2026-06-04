# 🛒 ShopKaro - India Ka Apna Bazaar
### Full-Featured E-Commerce Website (Django + Python)

---

## 📋 YE WEBSITE MEIN KYA HAI?

✅ **Homepage** - Banner slider, categories, deals, featured products  
✅ **Product Listing** - Filters (price, rating, brand), sorting, pagination  
✅ **Product Detail** - Multiple images, variants (size/color), reviews & ratings  
✅ **Search** - Search across products, brands, tags  
✅ **Login / Register** - Full auth system with seller registration  
✅ **Add to Cart** - AJAX based, quantity update, remove  
✅ **Wishlist** - Save favorite products  
✅ **Checkout** - Address selection, multiple payment methods (COD/UPI/Card/NetBanking)  
✅ **Orders** - Track orders, cancel orders, order history  
✅ **User Profile** - Edit profile, manage addresses  
✅ **Seller System** - Seller registration, seller dashboard, add products  
✅ **Admin Panel** - Full Django admin for managing everything  

---

## 🚀 SETUP KAISE KARO (Step by Step)

### Step 1: Python Install karo
Python 3.10+ chahiye: https://python.org/downloads

### Step 2: Is folder mein jao
```bash
cd shopkaro
```

### Step 3: Virtual environment banao (recommended)
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 4: Requirements install karo
```bash
pip install -r requirements.txt
```

### Step 5: Auto setup run karo (DATABASE + SAMPLE DATA)
```bash
python setup.py
```

### Step 6: Server start karo
```bash
python manage.py runserver
```

### Step 7: Browser mein kholo
```
Website:     http://127.0.0.1:8000/
Admin Panel: http://127.0.0.1:8000/admin/
```

---

## 🔐 LOGIN CREDENTIALS

| Account | Username | Password |
|---------|----------|----------|
| Admin (Full Access) | admin | admin123 |
| Demo Seller | seller1 | seller123 |

---

## 📁 FOLDER STRUCTURE

```
shopkaro/
├── manage.py          # Django management
├── setup.py           # Auto setup script
├── requirements.txt   # Dependencies
├── db.sqlite3         # Database (auto created)
├── media/             # Uploaded images
├── static/            # CSS, JS files
├── templates/         # HTML templates
│   ├── base.html
│   └── store/
│       ├── home.html
│       ├── product_list.html
│       ├── product_detail.html
│       ├── cart.html
│       ├── checkout.html
│       ├── orders.html
│       ├── wishlist.html
│       ├── profile.html
│       ├── login.html
│       ├── register.html
│       ├── seller_dashboard.html
│       └── add_product.html
├── shopkaro/          # Main project config
│   ├── settings.py
│   └── urls.py
└── store/             # Main app
    ├── models.py      # All database models
    ├── views.py       # All page logic
    ├── urls.py        # URL routing
    ├── admin.py       # Admin config
    └── context_processors.py
```

---

## 🛠️ ADMIN PANEL SE KYA KAR SAKTE HO?

1. **Products** add/edit karo with images
2. **Categories** manage karo (parent/sub categories)
3. **Banners** homepage ke liye add karo
4. **Orders** status update karo
5. **Sellers** approve karo
6. **Coupons** create karo
7. **Users** manage karo

---

## 💳 PAYMENT METHODS

- 💵 Cash on Delivery (COD)
- 📱 UPI Payment
- 💳 Credit/Debit Card
- 🏦 Net Banking
- 👛 Wallet

> **Note:** Payment gateway (Razorpay) integrate karne ke liye:
> `pip install razorpay` aur settings mein API keys add karo

---

## 📦 CATEGORIES (12 Main + 80+ Sub)

Electronics, Fashion, Home & Living, Beauty & Health,
Books, Sports, Toys & Games, Grocery, Automotive,
Jewellery, Furniture, Pet Supplies

---

## ❓ COMMON ISSUES

**Q: Images show nahi ho rahe?**  
A: `python manage.py runserver` se hi chalao, directly file mat kholo

**Q: Admin panel nahi khul raha?**  
A: `python setup.py` pehle run karo

**Q: Port already in use error?**  
A: `python manage.py runserver 8080` try karo

---

Made with ❤️ in India | ShopKaro © 2024
