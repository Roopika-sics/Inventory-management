from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from .models import Buyer
from django.contrib import messages
from categories.models import Category  
from products.models import Product, CartItem, Order, OrderItem
from categories.models import Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.db.models import Q
from django.http import HttpResponseForbidden
# Create your views here.

def buyer_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('buyer-register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Email already registered.")
            return redirect('buyer-register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user_type = 'buyer'
        user.save()
        buyer = Buyer.objects.create(user=user, phone_number=phone_number)
        buyer.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')  
    
    return render(request, 'buyer/buyer_register.html')

def get_user_recommendations(user):
    cart_cats = CartItem.objects.filter(user=user).values_list('product__category', flat=True)
    order_cats = OrderItem.objects.filter(order__user=user).values_list('product__category', flat=True)
    categories = list(set(cart_cats) | set(order_cats))

    interacted_product_ids = set(
        CartItem.objects.filter(user=user).values_list('product__id', flat=True)
    ) | set(
        OrderItem.objects.filter(order__user=user).values_list('product__id', flat=True)
    )

    if categories:
        recommendations = Product.objects.filter(
            category__in=categories
        ).exclude(id__in=interacted_product_ids).distinct()[:5]
    else:
        # fallback to latest products
        recommendations = Product.objects.exclude(id__in=interacted_product_ids).order_by('-id')[:5]

    return recommendations


@login_required
@never_cache
def buyer_home(request):
    smartphones = Product.objects.filter(category__name='Smart Phone')
    smart_wantchs = Product.objects.filter(category__name='Smart Watches')
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    search_results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(brand_name__icontains=query) |
        Q(model_number__icontains=query)
    )

    recommendations = []
    if request.user.is_authenticated:
        recommendations = get_user_recommendations(request.user)
    
    return render(request, 'buyer/buyer_home.html', {
        'smartphones': smartphones,
        'categories': categories,
        'query': query,
        'search_results': search_results,
        'recommendations': recommendations,
        'smart_wantchs': smart_wantchs
        
        })
        

@login_required
@never_cache
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'buyer/product_detail.html', {'product': product})

@login_required
@never_cache
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        quantity = product.stock

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if product.stock > 0:
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()
        product.stock -= quantity
        product.save()
        messages.success(request, "Product added to cart.")
    else:
        messages.error(request, "Product is out of stock.")
        return redirect('product-detail', pk=product_id)

    return redirect('product-detail', pk=product_id)

@login_required
@never_cache
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'buyer/cart.html', {'cart_items': cart_items, 'total': total})



@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        total = sum(item.product.base_price * item.quantity for item in cart_items)
        
       
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f"Not enough stock for {item.product.name}.")
                return redirect('cart')

        order = Order.objects.create(user=request.user, delivery_address=address, total_price=total)
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.base_price
            )
            
            item.product.stock -= item.quantity
            item.product.save()
        
        cart_items.delete()

        return render(request, 'buyer/order_success.html', {'order': order})

    total_price = sum(item.product.base_price * item.quantity for item in cart_items)
    return render(request, 'buyer/place_order.html', {'cart_items': cart_items, 'total_price': total_price})


def update_cart_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            new_quantity = data.get('quantity')

            if not item_id or not new_quantity:
                return JsonResponse({'error': 'Missing item ID or quantity'}, status=400)

            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            product = cart_item.product

            if new_quantity > 0 and new_quantity <= product.stock:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                return JsonResponse({'error': 'Invalid quantity'}, status=400)

    
            cart_items = CartItem.objects.filter(user=request.user)
            total = sum(item.product.price * item.quantity for item in cart_items)

            return JsonResponse({'message': 'Quantity updated', 'total': total})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


# def search_products(request):
#     query = request.GET.get('q', '')
#     search_results = Product.objects.filter(
#         Q(name__icontains=query) |
#         Q(description__icontains=query) |
#         Q(brand_name__icontains=query) |
#         Q(model_number__icontains=query)
#     )

#     recommendations = []
#     if request.user.is_authenticated:
#         recommendations = get_user_recommendations(request.user)

#     return render(request, 'buyer/buyer_home.html', {
#         'query': query,
#         'search_results': search_results,
#         'recommendations': recommendations,
#     })


def smart_phones(request):
    return render(request, 'buyer/smartphones.html')

def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'buyer/Category_products.html', {
        'category': category,
        'products': products
    })

@login_required
def orders(request):
    status = request.GET.get('status')
    if status:
        orders = Order.objects.filter(user=request.user, status=status)
    else:
        orders = Order.objects.filter(user=request.user)

    return render(request, 'buyer/orders.html', {
        'orders': orders,
        'current_status': status or 'all'
    })

@login_required
def track_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Ensure only the owner can track
    if order.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this order.")

    # Handle cancellation
    if request.method == 'POST' and 'cancel' in request.POST:
        if order.status not in ['delivered', 'cancelled']:
            order.status = 'cancelled'
            order.save()
        return redirect('track_order', order_id=order.id)

    return render(request, 'buyer/track_order.html', {'order': order})