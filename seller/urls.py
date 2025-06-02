from django.urls import path
from . import views

urlpatterns = [
    path('seller_register/', views.seller_registration, name='seller_register'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
   
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('profile/edit/', views.edit_seller_profile, name='edit-seller-profile'),


]
