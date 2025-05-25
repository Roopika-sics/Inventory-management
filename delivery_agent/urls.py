from django.urls import path
from . import views

urlpatterns = [
 path('delivery_agent_register/', views.delivery_agent_register, name='delivery_agent_register'),
 path('delivery_agent_home/', views.delivery_agent_dashboard, name='delivery_agent_home'),
 path('delivery/requests/', views.delivery_requests, name='delivery_requests'),
 path('delivery/accept/<int:order_id>/', views.accept_order, name='accept_order'),
 path('delivery/reject/<int:order_id>/', views.reject_order, name='reject_order'),


]
