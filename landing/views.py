from django.shortcuts import render
from products.models import Product
from categories.models import Category
# Create your views here.

def landing_page(request):
    smartphones = Product.objects.filter(category__name='Smart Phone')
    categories = Category.objects.all()
    return render(request, 'landing/landing_page.html', {'smartphones': smartphones, 'categories': categories})
