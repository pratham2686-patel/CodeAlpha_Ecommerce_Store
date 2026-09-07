from .cart import Cart
from .models import Category, Wishlist

def cart(request):
    return {'cart': Cart(request)}

def categories(request):
    return {'all_categories': Category.objects.all()}

def wishlist(request):
    count = 0
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_count': count}



