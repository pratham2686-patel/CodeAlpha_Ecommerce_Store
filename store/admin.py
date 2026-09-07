from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'rating', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    list_editable = ['price', 'stock', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'city', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'paid', 'created_at']
    list_editable = ['status']
    inlines = [OrderItemInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
