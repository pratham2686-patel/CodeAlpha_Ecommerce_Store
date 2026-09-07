from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # Wishlist / Saved Items URLs
    path('wishlist/', views.wishlist_list, name='wishlist_list'),
    path('wishlist/add/<int:product_id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', views.wishlist_remove, name='wishlist_remove'),
    path('wishlist/move-to-cart/<int:product_id>/', views.wishlist_move_to_cart, name='wishlist_move_to_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/pdf/<int:order_id>/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
]
