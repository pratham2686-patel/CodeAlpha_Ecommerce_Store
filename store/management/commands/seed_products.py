from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds initial categories and products into database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        categories_data = [
            {'name': 'Audio & Headphones', 'slug': 'audio-headphones', 'description': 'Noise-canceling headphones, wireless earbuds, and high-fidelity speakers.', 'icon': 'fa-headphones'},
            {'name': 'Smartphones & Wearables', 'slug': 'smartphones-wearables', 'description': 'Latest smartphones, smartwatches, and fitness trackers.', 'icon': 'fa-mobile-screen-button'},
            {'name': 'Laptops & Computers', 'slug': 'laptops-computers', 'description': 'Ultra-thin laptops, gaming rigs, and workstation PCs.', 'icon': 'fa-laptop'},
            {'name': 'Smart Home & Gadgets', 'slug': 'smart-home-gadgets', 'description': 'Smart lighting, security cameras, and home automation.', 'icon': 'fa-house-signal'},
        ]

        cat_objs = {}
        for cat in categories_data:
            obj, created = Category.objects.get_or_create(
                slug=cat['slug'],
                defaults={'name': cat['name'], 'description': cat['description'], 'icon': cat['icon']}
            )
            cat_objs[cat['slug']] = obj

        products_data = [
            {
                'category': cat_objs['laptops-computers'],
                'name': 'QuantumBook Pro 16 M3 Max Laptop',
                'slug': 'quantumbook-pro-16-m3-max-laptop',
                'description': 'Flagship performance laptop with 16-core CPU, 40-core GPU, 32GB Unified Memory, 1TB SSD, and 120Hz Liquid Retina display.',
                'price': 1899.00,
                'rating': 4.9,
                'stock': 10,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['audio-headphones'],
                'name': 'AeroSound Pro ANC Wireless Headphones',
                'slug': 'aerosound-pro-anc-wireless-headphones',
                'description': 'Industry-leading Active Noise Cancellation (ANC) with 40-hour battery life, 3D spatial audio, and memory foam ear cushions.',
                'price': 249.99,
                'rating': 4.9,
                'stock': 15,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smartphones-wearables'],
                'name': 'NovaPulse Watch Ultra Series 7',
                'slug': 'novapulse-watch-ultra-series-7',
                'description': 'Advanced health smartwatch with titanium case, ECG monitoring, SPO2 oxygen sensor, GPS sports tracking, and 5-day battery.',
                'price': 299.95,
                'rating': 4.8,
                'stock': 22,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1580477371194-4593e3c7c6cf?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['laptops-computers'],
                'name': 'TitanGamer 34" Ultrawide Curved Monitor',
                'slug': 'titangamer-34-ultrawide-curved-monitor',
                'description': 'Immersive 165Hz WQHD curved gaming display with HDR400, 1ms response time, and USB-C 65W power delivery.',
                'price': 549.00,
                'rating': 4.9,
                'stock': 8,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smart-home-gadgets'],
                'name': 'LuminaBeam Smart RGB Ambient Lamp',
                'slug': 'luminabeam-smart-rgb-ambient-lamp',
                'description': 'Smart LED desk lamp with Alexa/Google voice control, wireless phone charging pad, and 16 million RGB color scenes.',
                'price': 79.50,
                'rating': 4.7,
                'stock': 30,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1608156639585-b3a032ef9689?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['audio-headphones'],
                'name': 'SonicPulse Pro Noise-Canceling Earbuds',
                'slug': 'sonicpulse-pro-noise-canceling-earbuds',
                'description': 'Crystal-clear call quality with triple beamforming mics, IPX7 waterproof rating, and wireless charging case.',
                'price': 139.00,
                'rating': 4.7,
                'stock': 40,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1632200004922-bc18602c79fc?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smartphones-wearables'],
                'name': 'Horizon Fold 5G Smartphone',
                'slug': 'horizon-fold-5g-smartphone',
                'description': 'Revolutionary folding smartphone with 7.6" Dynamic AMOLED inner screen, 200MP camera, and 5000mAh dual battery.',
                'price': 1199.00,
                'rating': 4.8,
                'stock': 12,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smart-home-gadgets'],
                'name': 'CyberCam 4K AI Security System',
                'slug': 'cybercam-4k-ai-security-system',
                'description': 'AI-driven person and vehicle detection, color night vision, 2-way audio, and encrypted cloud/local storage.',
                'price': 99.99,
                'rating': 4.6,
                'stock': 18,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['laptops-computers'],
                'name': 'VaporCool RGB Mechanical Gaming Keyboard',
                'slug': 'vaporcool-rgb-mechanical-gaming-keyboard',
                'description': 'Hot-swappable mechanical switches, per-key RGB lighting, solid aluminum chassis, and detachable braided USB-C cable.',
                'price': 149.99,
                'rating': 4.9,
                'stock': 25,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1632078056157-f7eb9c54e9cc?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['laptops-computers'],
                'name': 'Apex Wireless 26K DPI Gaming Mouse',
                'slug': 'apex-wireless-26k-dpi-gaming-mouse',
                'description': 'Ultra-lightweight 58g ergonomic gaming mouse with 26,000 DPI optical sensor and 100-hour battery life.',
                'price': 89.99,
                'rating': 4.8,
                'stock': 35,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1616296425622-4560a2ad83de?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['audio-headphones'],
                'name': 'SoundStorm Cinema 5.1 Soundbar System',
                'slug': 'soundstorm-cinema-51-soundbar-system',
                'description': 'Dolby Atmos 5.1 channel home theater soundbar with wireless subwoofer and Bluetooth 5.3 streaming.',
                'price': 349.99,
                'rating': 4.8,
                'stock': 14,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smart-home-gadgets'],
                'name': 'VoltCharge 100W PD Power Bank 25000mAh',
                'slug': 'voltcharge-100w-pd-power-bank-25000mah',
                'description': '100W Power Delivery fast-charging battery pack capable of powering laptops, tablets, and phones simultaneously.',
                'price': 59.50,
                'rating': 4.7,
                'stock': 50,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1505236273191-1dce886b01e9?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smart-home-gadgets'],
                'name': 'SmartTouch Biometric Door Lock',
                'slug': 'smarttouch-biometric-door-lock',
                'description': 'Keyless entry door lock with 3D fingerprint scanner, digital touchscreen keypad, and mobile app access.',
                'price': 179.00,
                'rating': 4.8,
                'stock': 16,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1578319439584-104c94d37305?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smartphones-wearables'],
                'name': 'PulseFit Active Fitness Tracker',
                'slug': 'pulsefit-active-fitness-tracker',
                'description': 'Waterproof fitness band with continuous heart rate monitor, 14 workout modes, and 14-day battery runtime.',
                'price': 69.99,
                'rating': 4.6,
                'stock': 45,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smart-home-gadgets'],
                'name': 'CineView 4K Smart Laser Projector',
                'slug': 'cineview-4k-smart-laser-projector',
                'description': 'Ultra-short throw 4K laser home theater projector with built-in Harman Kardon speakers and Android TV.',
                'price': 799.00,
                'rating': 4.9,
                'stock': 6,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1629131726692-1accd0c53ce0?w=800&auto=format&fit=crop&q=80'
            },
            {
                'category': cat_objs['smart-home-gadgets'],
                'name': 'SkyDrone 4K HDR Camera Drone',
                'slug': 'skydrone-4k-hdr-camera-drone',
                'description': 'Foldable 4K HDR camera drone with 3-axis gimbal, 45-minute flight time, and 10km HD video transmission.',
                'price': 899.00,
                'rating': 4.9,
                'stock': 9,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1514598800938-f7125ea1aa1c?w=800&auto=format&fit=crop&q=80'
            }
        ]

        for p in products_data:
            Product.objects.get_or_create(
                slug=p['slug'],
                defaults=p
            )

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with categories and products!'))
