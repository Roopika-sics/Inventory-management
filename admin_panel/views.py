from django.shortcuts import render, redirect, get_object_or_404
from seller.models import Seller

# Create your views here.


def dashboard(request):
    sellers_count = Seller.objects.count()
    sellers_request_count = Seller.objects.filter(is_approved=False, is_rejected=False).count()
    context = {
        'sellers_count': sellers_count,
        'sellers_request_count': sellers_request_count
    }
    return render(request, 'admin_panel/admin_dashboard.html', context)

def seller_requests(request):
    sellers = Seller.objects.filter(is_approved=False, is_rejected=False)
    return render(request, 'admin_panel/sellers_requests.html', {'sellers': sellers})

def seller_request_detail(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            seller.is_approved = True
            seller.save()
        elif action == 'reject':
            reason = request.POST.get('reason', '')
            seller.is_rejected = True
            seller.rejection_reason = reason
            seller.save()
        return redirect('seller_requests')

    return render(request, 'admin_panel/seller_request_viewmore.html', {'seller': seller})

def seller_view(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    return render(request, 'admin_panel/seller_view.html', {'seller': seller})

def sellers_list(request):
    sellers = Seller.objects.all()
    return render(request, 'admin_panel/sellers.html', {'sellers': sellers})