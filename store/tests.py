from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product, Order, OrderItem, Wishlist

class StoreModelAndBaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='john', password='password123')
        self.category = Category.objects.create(
            name='Test Electronics',
            slug='test-electronics',
            description='Test category description',
            icon='fa-plug'
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name='AeroSound Speaker',
            slug='aerosound-speaker',
            description='A test speaker item',
            price=119.00,
            rating=4.8,
            stock=5,
            is_featured=True
        )
        self.out_of_stock_product = Product.objects.create(
            category=self.category,
            name='Sold Out Tech',
            slug='sold-out-tech',
            description='An item that is sold out',
            price=99.99,
            rating=4.5,
            stock=0,
            is_featured=False
        )

    def test_cart_add_requires_login(self):
        response = self.client.post(reverse('store:cart_add', args=[self.product1.id]), {'quantity': 1})
        self.assertEqual(response.status_code, 302)

    def test_out_of_stock_validation(self):
        self.client.login(username='john', password='password123')
        # Attempting to add out of stock item should fail
        response = self.client.post(reverse('store:cart_add', args=[self.out_of_stock_product.id]), {'quantity': 1})
        self.assertEqual(response.status_code, 302)
        # Should redirect back to product detail page with warning message
        self.assertEqual(self.out_of_stock_product.stock, 0)

    def test_stock_deduction_on_checkout(self):
        self.client.login(username='john', password='password123')
        
        # Add 2 units of product1 (initial stock 5)
        self.client.post(reverse('store:cart_add', args=[self.product1.id]), {'quantity': 2, 'override': False})
        
        checkout_data = {
            'full_name': 'john patel',
            'email': 'john@gmail.com',
            'phone_number': '+1 202-555-0168',
            'address': '742 Evergreen Terrace',
            'city': 'Springfield',
            'state': 'Illinois',
            'postal_code': '62704',
            'country': 'United States',
        }
        response = self.client.post(reverse('store:checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        # Refresh product from DB and verify stock was reduced from 5 to 3
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 3)

    def test_wishlist_add_and_move_to_cart(self):
        self.client.login(username='john', password='password123')
        
        # Add product1 to wishlist
        res_add = self.client.get(reverse('store:wishlist_add', args=[self.product1.id]))
        self.assertEqual(res_add.status_code, 302)
        self.assertEqual(Wishlist.objects.filter(user=self.user, product=self.product1).count(), 1)

        # Move from wishlist to cart
        res_move = self.client.get(reverse('store:wishlist_move_to_cart', args=[self.product1.id]))
        self.assertEqual(res_move.status_code, 302)
        self.assertEqual(Wishlist.objects.filter(user=self.user, product=self.product1).count(), 0)
