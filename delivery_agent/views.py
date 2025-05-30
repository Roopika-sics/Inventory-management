from django.shortcuts import render, redirect
from accounts.models import User
from .models import DeliveryAgent, OrderVisibility
from products.models import Order
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST

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

        return redirect('login')

    return render(request, 'delivery_agent/agent_register.html')

def delivery_agent_dashboard(request):
    return render(request, 'delivery_agent/agent_dashboard.html')

def delivery_requests(request):
    agent = DeliveryAgent.objects.get(user=request.user)    
    status = request.GET.get('status')
    print('ststuss',status)

    rejected_orders = OrderVisibility.objects.filter(agent=agent, rejected=True).values_list('order_id', flat=True)
    print(rejected_orders)
    if status == 'placed':
        orders = Order.objects.filter(status='placed').exclude(assigned_to=agent)
    elif status == 'pending':
        orders = Order.objects.filter(status='pending', assigned_to=agent)
    elif status == 'delivered':
        orders = Order.objects.filter(status='delivered', assigned_to=agent)
    else:
        orders = []
    


    return render(request, 'delivery_agent/delivery_requests.html', {'orders': orders, 'status': status, 'rejected_orders': rejected_orders})

@login_required
def accept_order(request, order_id):
    agent = DeliveryAgent.objects.get(user=request.user)
    order = get_object_or_404(Order, id=order_id, is_assigned=False)

    order.assigned_to = agent
    order.is_assigned = True
    order.status = 'pending'
    order.save()

    return redirect(f"{reverse('delivery_requests')}?status=pending")

def reject_order(request, order_id):
    agent = DeliveryAgent.objects.get(user=request.user)
    order = get_object_or_404(Order, id=order_id)

    OrderVisibility.objects.create(order=order, agent=agent, rejected=True)
    return redirect('delivery_requests')

@login_required
def mark_as_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    agent = get_object_or_404(DeliveryAgent, user=request.user)

    if order.assigned_to == agent:
        order.status = 'delivered'
        order.save()

    return redirect('pending_deliveries')

@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, assigned_to__user=request.user)
    new_status = request.POST.get('new_status')

    if new_status in ['transit', 'delivered']:
        order.status = new_status
        order.save()

    return redirect(f"{reverse('delivery_requests')}?status=pending")

@require_POST
def report_order_issue(request, order_id):
    order = get_object_or_404(Order, id=order_id, assigned_to__user=request.user)

    issue_reason = request.POST.get('issue_reason')
    notes = request.POST.get('additional_notes')

    order.issue_reason = f"{issue_reason} - {notes}"
    order.status = 'pending'
    order.save()

    return redirect(f"{reverse('delivery_dashboard')}?status=pending")