from django.shortcuts import render, redirect
from accounts.models import User
from .models import DeliveryAgent, OrderVisibility
from products.models import Order
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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

def delivery_agent_dashboard(request):
    return render(request, 'delivery_agent/agent_dashboard.html')

def delivery_requests(request):
    agent = DeliveryAgent.objects.get(user=request.user)    

    rejected_orders = OrderVisibility.objects.filter(agent=agent, rejected=True).values_list('order_id', flat=True)
    orders = Order.objects.filter(is_assigned=False).exclude(id__in=rejected_orders).prefetch_related(
        'items__product__seller__seller_profile'
    )


    return render(request, 'delivery_agent/delivery_requests.html', {'orders': orders})

@login_required
def accept_order(request, order_id):
    agent = DeliveryAgent.objects.get(user=request.user)
    order = get_object_or_404(Order, id=order_id, is_assigned=False)

    order.assigned_to = agent
    order.is_assigned = True
    order.status = 'Accepted'
    order.save()

    return redirect('delivery_requests')

def reject_order(request, order_id):
    agent = DeliveryAgent.objects.get(user=request.user)
    order = get_object_or_404(Order, id=order_id)

    OrderVisibility.objects.create(order=order, agent=agent, rejected=True)
    return redirect('delivery_requests')