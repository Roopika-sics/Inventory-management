from django.shortcuts import render, redirect
from accounts.models import User
from .models import Buyer
from django.contrib import messages
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

