from django.shortcuts import render, redirect
from .models import Seller
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from products.models import Product
from categories.models import Category
from django.shortcuts import get_object_or_404

def seller_registration(request):
    if request.method == "POST":
    
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password') 
        business_name = request.POST.get('displayname')
        business_address = request.POST.get('businessaddress')
        business_type = request.POST.get('businesstype')
        registration_number = request.POST.get('registernumber')
        validation_doc = request.FILES.get('validationdoc')

      
        user = User.objects.create_user(username=full_name, email=email, password=password)
        user.user_type = 'seller'
        user.save()

        seller = Seller.objects.create(
            user=user,
            phone_number=phone,
            business_name=business_name,
            business_type=business_type,
            business_address=business_address,
            registration_number=registration_number,
            validation_document=validation_doc
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'seller/seller_registration.html')

@login_required
@never_cache
def seller_dashboard(request):
    return render(request, 'seller/seller_dashboard.html')

@login_required
@never_cache
def seller_profile(request):
    seller = request.user.seller_profile
    return render(request, 'seller/seller_profile.html', {'seller': seller})



@login_required
@never_cache
def edit_seller_profile(request):
    seller = request.user.seller_profile

    if request.method == 'POST':
        seller.user.username = request.POST.get('username')
        seller.user.email = request.POST.get('email')
        seller.user.save()
        seller.phone_number = request.POST.get('phone_number')
        seller.business_name = request.POST.get('business_name')
        seller.business_type = request.POST.get('business_type')
        seller.business_address = request.POST.get('business_address')
        seller.registration_number = request.POST.get('registration_number')

        if request.FILES.get('validation_document'):
            seller.validation_document = request.FILES.get('validation_document')

        seller.save()
        return redirect('seller_profile')

    return render(request, 'seller/edit_seller_pro.html', {'seller': seller})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        brand_name = request.POST.get('brand_name')
        model_number = request.POST.get('model_number')
        category_id = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        base_price = request.POST.get('base_price')
        discount = request.POST.get('discount')
        image = request.FILES.get('image')
        stock = request.POST.get('stock')

        category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(
            seller=request.user,
            name=name,
            description=description,
            brand_name=brand_name,
            model_number=model_number,
            category=category,
            sub_category=sub_category,
            base_price=base_price,
            discount=discount,
            image=image,
            stock=stock
        )
        return redirect('seller_dashboard')
    
    categories = Category.objects.all()
    return render(request, 'seller/add_product.html', {'categories': categories})

def view_products(request):
    status=request.GET.get('status')
    print(status)
    if status:
        products = Product.objects.filter(seller=request.user, status=status)
    else:
        products = Product.objects.filter(seller=request.user)
    return render(request, 'seller/view_products.html', {'products': products, 'current_status': status or 'all'})