from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from .models import Buyer
from django.contrib import messages
from products.models import Product, CartItem
from categories.models import Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
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


@login_required
@never_cache
def buyer_home(request):
    smartphones = Product.objects.filter(category__name='Smart Phone')
    categories = Category.objects.all()
    return render(request, 'buyer/buyer_home.html', {'smartphones': smartphones, 'categories': categories})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'buyer/product_detail.html', {'product': product})

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

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'buyer/cart.html', {'cart_items': cart_items, 'total': total})