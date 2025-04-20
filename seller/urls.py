from django.urls import path
from . import views

urlpatterns = [
    path('seller_register/', views.seller_registration, name='seller_register'),
    path('seller_home/', views.seller_home, name='seller_home'),
    path('profile/', views.seller_profile, name='seller-profile'),
    path('profile/edit/', views.edit_seller_profile, name='edit-seller-profile'),


]
