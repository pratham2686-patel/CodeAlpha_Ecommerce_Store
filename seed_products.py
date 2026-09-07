import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_store.settings')
django.setup()

from store.models import Category, Product

# Create categories if they don't exist
audio, _ = Category.objects.get_or_create(name='Audio & Headphones', slug='audio-headphones', defaults={'icon': 'fa-headphones'})
laptops, _ = Category.objects.get_or_create(name='Laptops & Computers', slug='laptops-computers', defaults={'icon': 'fa-laptop'})
smart_home, _ = Category.objects.get_or_create(name='Smart Home & Gadgets', slug='smart-home-gadgets', defaults={'icon': 'fa-house-signal'})
wearables, _ = Category.objects.get_or_create(name='Smartphones & Wearables', slug='smartphones-wearables', defaults={'icon': 'fa-mobile-screen-button'})

print("Categories created successfully!")

products_data = [
    # Audio
    {
        'category': audio,
        'name': 'Sony WH-1000XM5 Headphones',
        'slug': 'sony-wh-1000xm5',
        'description': 'Premium noise canceling headphones.',
        'price': 399.00,
        'original_price': 499.00,
        'rating': 4.9,
        'stock': 20,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1761120359417-e7b609cef1ca?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': audio,
        'name': 'Bose QC Ultra Earbuds',
        'slug': 'bose-qc-ultra',
        'description': 'Wireless noise canceling earbuds.',
        'price': 299.00,
        'original_price': 379.00,
        'rating': 4.8,
        'stock': 18,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': audio,
        'name': 'JBL Pulse 5 Speaker',
        'slug': 'jbl-pulse-5',
        'description': 'Portable Bluetooth speaker with LED light show.',
        'price': 249.00,
        'original_price': 299.00,
        'rating': 4.6,
        'stock': 25,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1511499271651-073325718d90?w=800&auto=format&fit=crop&q=80'
    },

    # Laptops
    {
        'category': laptops,
        'name': 'MacBook Air M3 15-inch',
        'slug': 'macbook-air-m3',
        'description': 'Lightweight laptop with M3 chip.',
        'price': 1499.00,
        'original_price': 1799.00,
        'rating': 4.9,
        'stock': 10,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': laptops,
        'name': 'Dell XPS 16 4K OLED',
        'slug': 'dell-xps-16',
        'description': '4K OLED touchscreen laptop.',
        'price': 1899.00,
        'original_price': 2299.00,
        'rating': 4.7,
        'stock': 8,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': laptops,
        'name': 'ASUS ROG Zephyrus G16',
        'slug': 'asus-rog-zephyrus-g16',
        'description': 'Gaming laptop with RTX 4070.',
        'price': 2199.00,
        'original_price': 2599.00,
        'rating': 4.8,
        'stock': 6,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1618424181497-157f25b6ddd5?w=800&auto=format&fit=crop&q=80'
    },

    # Smart Home
    {
        'category': smart_home,
        'name': 'SkyDrone 4K HDR Camera Drone',
        'slug': 'skydrone-4k-hdr',
        'description': 'Professional camera drone.',
        'price': 899.00,
        'original_price': 1099.00,
        'rating': 4.9,
        'stock': 8,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': smart_home,
        'name': 'Nest Thermostat 3rd Gen',
        'slug': 'nest-thermostat-3',
        'description': 'Smart energy-saving thermostat.',
        'price': 249.00,
        'original_price': 299.00,
        'rating': 4.6,
        'stock': 25,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': smart_home,
        'name': 'Philips Hue Starter Kit',
        'slug': 'philips-hue-starter',
        'description': 'Smart LED lighting system.',
        'price': 159.00,
        'original_price': 199.00,
        'rating': 4.5,
        'stock': 12,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1572613090232-224fa91e5394?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': smart_home,
        'name': 'Ring Doorbell Pro 2',
        'slug': 'ring-doorbell-pro-2',
        'description': 'HD video doorbell.',
        'price': 229.00,
        'original_price': 279.00,
        'rating': 4.8,
        'stock': 18,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1633194883650-df448a10d554?w=800&auto=format&fit=crop&q=80'
    },

    # Wearables
    {
        'category': wearables,
        'name': 'iPhone 16 Pro Max',
        'slug': 'iphone-16-pro-max',
        'description': 'Flagship iPhone with A18 Pro chip.',
        'price': 1199.00,
        'original_price': 1399.00,
        'rating': 4.9,
        'stock': 12,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': wearables,
        'name': 'Samsung S24 Ultra',
        'slug': 'galaxy-s24-ultra',
        'description': 'Samsung flagship with S Pen.',
        'price': 1299.00,
        'original_price': 1499.00,
        'rating': 4.8,
        'stock': 10,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1634403665481-74948d815f03?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': wearables,
        'name': 'OnePlus 12 5G',
        'slug': 'oneplus-12',
        'description': 'Flagship phone with Hasselblad camera.',
        'price': 899.00,
        'original_price': 1099.00,
        'rating': 4.7,
        'stock': 15,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': wearables,
        'name': 'Pixel 9 Pro XL',
        'slug': 'pixel-9-pro-xl',
        'description': 'Google flagship with AI features.',
        'price': 1099.00,
        'original_price': 1299.00,
        'rating': 4.8,
        'stock': 8,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': wearables,
        'name': 'Apple Watch Ultra 2',
        'slug': 'apple-watch-ultra-2',
        'description': 'Titanium smartwatch with GPS.',
        'price': 799.00,
        'original_price': 999.00,
        'rating': 4.9,
        'stock': 15,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1633339257099-3697720c2c3c?w=800&auto=format&fit=crop&q=80'
    },

    # Extra
    {
        'category': smart_home,
        'name': 'Samsung 65-inch 4K TV',
        'slug': 'samsung-65-4k-tv',
        'description': 'Neo QLED 4K smart TV.',
        'price': 1299.00,
        'original_price': 1599.00,
        'rating': 4.8,
        'stock': 5,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1601944177325-f8867652837f?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': laptops,
        'name': 'Kindle Scribe 10.2"',
        'slug': 'kindle-scribe',
        'description': 'E-Reader with built-in stylus.',
        'price': 339.00,
        'original_price': 399.00,
        'rating': 4.7,
        'stock': 20,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1539376248633-cf94fa8b7bd8?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': laptops,
        'name': 'Canon EOS R5 Camera',
        'slug': 'canon-eos-r5',
        'description': 'Mirrorless camera with 8K video.',
        'price': 2499.00,
        'original_price': 2999.00,
        'rating': 4.9,
        'stock': 3,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1571689936008-083b32a9dcca?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': laptops,
        'name': 'Nintendo Switch OLED',
        'slug': 'nintendo-switch-oled',
        'description': 'Gaming console with OLED screen.',
        'price': 349.00,
        'original_price': 399.00,
        'rating': 4.8,
        'stock': 15,
        'is_featured': False,
        'image_url': 'https://images.unsplash.com/photo-1655560378428-7605bda51749?w=800&auto=format&fit=crop&q=80'
    },
    {
        'category': audio,
        'name': 'SoundStorm 5.1 Soundbar',
        'slug': 'soundstorm-5-1',
        'description': 'Surround sound system.',
        'price': 349.99,
        'original_price': 399.99,
        'rating': 4.8,
        'stock': 13,
        'is_featured': True,
        'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80'
    },
]

# Insert products into database
for data in products_data:
    product, created = Product.objects.get_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        print(f"Added: {product.name}")
    else:
        print(f"Already exists: {product.name}")

print("Bulk seeding completed!")