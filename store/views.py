from django.conf import settings
from django.core.mail import send_mail
import io
from decimal import Decimal
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.urls import reverse

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from .models import Category, Product, Order, OrderItem, Wishlist,Review
from .cart import Cart
from .forms import SignUpForm, OrderCreateForm, CartAddProductForm ,ReviewForm





def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    
    # Get search and sort parameters
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    
    # Get filter parameters
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_rating = request.GET.get('min_rating', '')
    in_stock = request.GET.get('in_stock', '')

    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search filter
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )

    # Price range filters
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except:
            pass

    # Rating filter
    if min_rating:
        try:
            products = products.filter(rating__gte=Decimal(min_rating))
        except:
            pass

    # In Stock filter
    if in_stock == 'true':
        products = products.filter(stock__gt=0)

    # Sort by (updated with Newest)
    if sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    # PAGINATION LOGIC (8 products per page)
    paginator = Paginator(products, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    recent_ids = request.session.get('recently_viewed', [])
    recent_products = Product.objects.filter(id__in=recent_ids)

    
    context = {
        'category': category,
        'categories': categories,
        'products': page_obj,  # Pass page_obj instead of products
        'query': query,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'in_stock': in_stock,
        'recently_viewed_products': recent_products,
    }
    return render(request, 'store/product_list.html', context)




def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # NEW: Recently Viewed Products Logic (Session based)
    recent_products = request.session.get('recently_viewed', [])
    
    # Add current product ID to the list (if not already there)
    if product.id not in recent_products:
        recent_products.insert(0, product.id)
        # Keep only last 4 products
        recent_products = recent_products[:12]
        request.session['recently_viewed'] = recent_products
        request.session.modified = True

    # Fetch the actual products from database
    recent_product_objects = Product.objects.filter(id__in=recent_products).exclude(id=product.id)

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
        # NEW: Pass recently viewed products to template
        'recently_viewed_products': recent_product_objects,
    }
    return render(request, 'store/product_detail.html', context)

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'store/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    # Validation 1: Only logged-in users can add products to cart
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'redirect_url': reverse('store:login'),
                'message': 'Please log in to add products to your cart.'
            }, status=401)
        messages.warning(request, "Please log in to add products to your cart.")
        return redirect('store:login')

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Validation 2: Fresh Stock Check from Database
    product.refresh_from_db()
    if not product.is_in_stock or product.stock <= 0:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Sorry, "{product.name}" is currently out of stock and cannot be purchased.'
            }, status=400)
        messages.warning(request, f'Sorry, "{product.name}" is currently out of stock and cannot be purchased.')
        return redirect(product.get_absolute_url())

    form = CartAddProductForm(request.POST)
    quantity_to_add = 1
    override = False

    if form.is_valid():
        cd = form.cleaned_data
        quantity_to_add = cd['quantity']
        override = cd['override']

    # Validation 3: Quantity vs Fresh Stock Validation
    existing_qty = cart.cart.get(str(product.id), {}).get('quantity', 0)
    total_requested = quantity_to_add if override else (existing_qty + quantity_to_add)

    if total_requested > product.stock:
        err_msg = f'Only {product.stock} units of "{product.name}" available in stock.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': err_msg}, status=400)
        messages.warning(request, err_msg)
        return redirect('store:cart_detail')

    cart.add(
        product=product,
        quantity=quantity_to_add,
        override_quantity=override
    )
    messages.success(request, f'"{product.name}" added to cart!')
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_total': len(cart)})
        
    return redirect('store:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.POST.get('save_to_wishlist'):
        # Validation: only logged-in users can save to wishlist
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to save items to your Wishlist.")
            return redirect('store:cart_detail')

        item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, f'"{product.name}" saved to Wishlist!')
        else:
            messages.info(request, f'"{product.name}" already in Wishlist.')
    else:
        messages.info(request, f'"{product.name}" removed from cart.')

    return redirect('store:cart_detail')


# --- Wishlist / Saved Items Views & Validations ---

@login_required
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

def wishlist_add(request, product_id):
    # Validation 1: Login Requirement
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'redirect_url': reverse('store:login'),
                'message': 'Please log in to save products for later.'
            }, status=401)
        messages.warning(request, "Please log in to save products for later.")
        return redirect('store:login')

    product = get_object_or_404(Product, id=product_id)
    
    # Validation 2: Prevent Duplicate Saved Items
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        msg = f'"{product.name}" saved to your Wishlist'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'action': 'added', 'message': msg})
        messages.success(request, msg)
    else:
        # Toggle off if already saved
        item.delete()
        msg = f'"{product.name}" removed from your Wishlist.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'action': 'removed', 'message': msg})
        messages.info(request, msg)

    return redirect('store:wishlist_list')

@login_required
def wishlist_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.info(request, f'"{product.name}" removed from saved items.')
    return redirect('store:wishlist_list')

@login_required
def wishlist_move_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Validation 3: Stock Availability Check before moving item to cart
    product.refresh_from_db()
    if not product.is_in_stock or product.stock <= 0:
        messages.error(request, f'Sorry, "{product.name}" is currently out of stock and cannot be moved to cart.')
        return redirect('store:wishlist_list')

    cart = Cart(request)
    cart.add(product=product, quantity=1)
    
    # Remove from wishlist once added to cart
    Wishlist.objects.filter(user=request.user, product=product).delete()
    
    messages.success(request, f'"{product.name}" moved to cart successfully!')
    return redirect('store:product_list')


def checkout(request):
    cart = Cart(request)
    
    # Validation: Cart Empty Check
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add products before checking out!")
        return redirect('store:product_list')

    # Validation: Fresh DB Stock Verification before completing purchase
    for item in cart:
        db_product = Product.objects.get(id=item['product'].id)
        if db_product.stock < item['quantity']:
            if db_product.stock == 0:
                messages.error(request, f'Sorry, "{db_product.name}" is out of stock. Please remove it from your cart.')
            else:
                messages.error(request, f'Sorry, "{db_product.name}" only has {db_product.stock} items in stock. Please reduce quantity.')
            return redirect('store:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            # Atomic Stock Deduction directly on fresh Database records
            for item in cart:
                db_product = Product.objects.get(id=item['product'].id)
                db_product.stock = max(0, db_product.stock - item['quantity'])
                db_product.save()

                OrderItem.objects.create(
                    order=order,
                    product=db_product,
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()
            messages.success(request, "Order placed successfully!")
            return redirect('store:order_success', order_id=order.id)
        else:
            messages.error(request, "Please correct the highlighted errors in the form below.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user_orders = None
    account_total_spent = Decimal('0.00')
    all_user_items = []

    if request.user.is_authenticated and order.user == request.user:
        user_orders = Order.objects.filter(user=request.user)
        account_total_spent = sum(o.total_price for o in user_orders)
        all_user_items = OrderItem.objects.filter(order__user=request.user).select_related('product', 'order')

    # Send Order Confirmation Email
    try:
        # Python string ke liye date ko format karna zaroori hai
        delivery_start_str = order.delivery_start.strftime("%b %d, %Y")
        delivery_end_str = order.delivery_end.strftime("%b %d, %Y")

        subject = f"Order Confirmed #{order.id} - ElectroMart"
        message = f"""
        Dear {order.full_name},

        Thank you for shopping with ElectroMart!

        Your order #{order.id} has been placed successfully.
        Total Amount: ${order.total_price}
        Estimated Delivery: {delivery_start_str} to {delivery_end_str}

        We will notify you once your order is shipped.

        Regards,
        ElectroMart Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [order.email]
        
        send_mail(subject, message, from_email, recipient_list)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed: {e}")

    context = {
        'order': order,
        'user_orders': user_orders,
        'account_total_spent': account_total_spent,
        'all_user_items': all_user_items,
    }
    return render(request, 'store/order_success.html', context)

def download_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    is_preview = request.GET.get('preview') == '1'
    
    # Permission Validation: Ensure users access only their own orders
    if request.user.is_authenticated and order.user and order.user != request.user:
        messages.error(request, "Unauthorized access to invoice.")
        return redirect('store:product_list')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=10
    )
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontName='Helvetica-Bold')

    elements.append(Paragraph("ElectroMart - Official Order Invoice & Purchase History", title_style))
    
    # Render Exact Purchase Date AND Time
    formatted_datetime = order.created_at.strftime('%B %d, %Y at %I:%M %p')
    elements.append(Paragraph(f"<b>Invoice ID:</b> #{order.id} &nbsp;|&nbsp; <b>Date & Time:</b> {formatted_datetime}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Billed To & Address Table
    phone_display = order.phone_number if order.phone_number else 'N/A'
    state_display = f", {order.state}" if order.state else ''
    country_display = order.country if order.country else 'United States'

    billing_info = [
        [Paragraph("<b>Customer Details</b>", bold_style), Paragraph("<b>Shipping Address</b>", bold_style)],
        [
            Paragraph(f"<b>Name:</b> {order.full_name}<br/><b>Email:</b> {order.email}<br/><b>Phone:</b> {phone_display}", styles['Normal']),
            Paragraph(f"<b>Address:</b> {order.address}<br/><b>City/State:</b> {order.city}{state_display}<br/><b>Zip/Country:</b> {order.postal_code}, {country_display}", styles['Normal'])
        ]
    ]

    billing_table = Table(billing_info, colWidths=[260, 260])
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(billing_table)
    elements.append(Spacer(1, 20))

    table_data = [["Order #", "Product", "Unit Price", "Qty", "Subtotal"]]
    grand_total = Decimal('0.00')

    if request.user.is_authenticated and order.user == request.user:
        user_orders = Order.objects.filter(user=request.user)
        for ord_item in user_orders:
            grand_total += ord_item.total_price
            for item in ord_item.items.all():
                table_data.append([
                    f"#{ord_item.id}",
                    item.product.name,
                    f"${item.price}",
                    str(item.quantity),
                    f"${item.get_cost()}"
                ])
    else:
        grand_total = order.total_price
        for item in order.items.all():
            table_data.append([
                f"#{order.id}",
                item.product.name,
                f"${item.price}",
                str(item.quantity),
                f"${item.get_cost()}"
            ])

    table_data.append(["", "", "", "Total Spent:", f"${grand_total}"])

    items_table = Table(table_data, colWidths=[65, 235, 75, 45, 100])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-2), 0.5, colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (3,-1), (4,-1), colors.HexColor('#4f46e5')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 25))
    elements.append(Paragraph("<i>Thank you for shopping with ElectroMart! For support, contact support@electromart.com</i>", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    disposition = 'inline' if is_preview else 'attachment'
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'{disposition}; filename="Invoice_Order_#{order.id}.pdf"'
    return response

def register_request(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to ElectroMart, {user.username}! Registration successful.")
            return redirect('store:product_list')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'store/register.html', {'form': form})

def login_request(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('store:product_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect('store:product_list')

@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user)
    total_spent = sum(order.total_price for order in orders)
    total_items_purchased = sum(item.quantity for order in orders for item in order.items.all())

    context = {
        'orders': orders,
        'total_spent': total_spent,
        'total_items_purchased': total_items_purchased,
    }
    return render(request, 'store/profile.html', context)



@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if user already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.warning(request, "You have already reviewed this product!")
        return redirect('store:product_detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Thank you! Your review has been posted.")
        else:
            messages.error(request, "Please choose a valid rating before submitting your review.")
        return redirect('store:product_detail', slug=product.slug)

    # The review form is embedded directly on the product detail page,
    # so a plain GET request here just sends the user back there.
    return redirect('store:product_detail', slug=product.slug)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Check: Sirf review ka owner hi edit kar sakta hai
    if review.user != request.user:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('store:product_detail', slug=review.product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated successfully!")
            return redirect('store:product_detail', slug=review.product.slug)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'store/edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Check: Sirf review ka owner hi delete kar sakta hai
    if review.user != request.user:
        messages.error(request, "You are not authorized to delete this review.")
        return redirect('store:product_detail', slug=review.product.slug)

    if request.method == 'POST':
        product_slug = review.product.slug
        review.delete()
        messages.success(request, "Your review has been deleted successfully!")
        return redirect('store:product_detail', slug=product_slug)

    return render(request, 'store/delete_review.html', {'review': review})

def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )[:8]  # Max 8 suggestions
        data = [{
            'name': p.name,
            'slug': p.slug,
            'price': str(p.price),
            'image': p.image_url
        } for p in products]
        return JsonResponse({'products': data})
    return JsonResponse({'products': []})