from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.buyer_register, name='buyer-register'),
    path('home/', views.buyer_home, name='buyer-home'),
]
