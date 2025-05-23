from django.shortcuts import render, redirect
from .models import Seller
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

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

        return redirect('landing_page')

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