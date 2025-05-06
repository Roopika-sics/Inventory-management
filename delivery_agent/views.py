from django.shortcuts import render, redirect
from accounts.models import User
from .models import DeliveryAgent
# Create your views here.

def delivery_agent_register(request):
    if request.method == "POST":
    
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        location = request.POST.get('location')
        pincode = request.POST.get('pincode')
        licence_number = request.POST.get('licencenumber')
        licence_expiry_date = request.POST.get('licenceexpirydate')
        driving_licence = request.FILES.get('drivinglicence')
        password = request.POST.get('password') 

        user = User.objects.create_user(username=full_name, email=email, password=password)
        user.user_type = 'delivery_agent'
        user.save()

        agent = DeliveryAgent.objects.create(
            user=user,
            phone=phone,
            city=city,
            location=location,
            pincode=pincode,
            licence_number=licence_number,
            licence_expiry_date=licence_expiry_date,
            driving_licence=driving_licence
        )

        return redirect('landing_page')

    return render(request, 'delivery_agent/agent_register.html')