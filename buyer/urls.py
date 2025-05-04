from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.buyer_register, name='buyer-register'),
    path('home/', views.buyer_home, name='buyer-home'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('place_order/' , views.place_order, name='place_order'),

]
