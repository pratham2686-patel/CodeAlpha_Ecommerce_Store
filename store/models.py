from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-box')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    stock = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    image_url = models.CharField(max_length=500, default='https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800&auto=format&fit=crop&q=80')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def is_in_stock(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        """Correctly computed % off, based on original_price vs price."""
        if self.original_price and self.original_price > self.price:
            return round((self.original_price - self.price) / self.original_price * 100)
        return 0

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total = sum([r.rating for r in reviews])
            return round(total / len(reviews), 1)
        return self.rating  # Default rating if no reviews


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    PAYMENT_CHOICES = [
        ('Credit / Debit Card', 'Credit / Debit Card'),
        ('UPI / NetBanking', 'UPI / NetBanking'),
        ('Cash on Delivery (COD)', 'Cash on Delivery (COD)'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='')
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Credit / Debit Card')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    paid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"
    @property
    def delivery_start(self):
        return self.created_at + timedelta(days=4)
    @property
    def delivery_end(self):
        return self.created_at + timedelta(days=7)

    @property
    def status_step(self):
        """Returns which tracking step (1-4) the order is currently at,
        for rendering the visual order-tracking timeline."""
        steps = {'Pending': 1, 'Processing': 2, 'Shipped': 3, 'Delivered': 4}
        return steps.get(self.status, 1)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"

    def get_cost(self):
        return self.price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wished_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.product.name}"
    
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5)
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')  # Ek user ek product par sirf ek review de sakta hai

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} stars)"