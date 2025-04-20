from django.urls import path
from . import views

urlpatterns = [
    path('seller_register/', views.seller_registration, name='seller_register'),
]
