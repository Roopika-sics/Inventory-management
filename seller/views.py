from django.shortcuts import render, redirect
from .models import Seller
from accounts.models import User

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
            full_name=full_name,
            email=email,
            phone_number=phone,
            business_name=business_name,
            business_type=business_type,
            business_address=business_address,
            registration_number=registration_number,
            validation_document=validation_doc
        )

        return redirect('landing_page')

    return render(request, 'seller/seller_registration.html')
