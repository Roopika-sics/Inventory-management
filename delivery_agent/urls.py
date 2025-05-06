from django.urls import path
from . import views

urlpatterns = [
 path('delivery_agent_register/', views.delivery_agent_register, name='delivery_agent_register'),


]
