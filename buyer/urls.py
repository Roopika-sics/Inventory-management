from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.buyer_register, name='buyer-register'),
    path('home/', views.buyer_home, name='buyer-home'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('place_order/' , views.place_order, name='place_order'),
    path('update-cart-item/', views.update_cart_item, name='update-cart-item'),
    path('remove_cart_item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('smart_phones/', views.smart_phones, name='smart_phones'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('orders/', views.orders, name='orders'),
    path('track-order/<int:order_id>/', views.track_order_view, name='track_order'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),

    # path('search/', views.search_products, name='search_products'),


]
