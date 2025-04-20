from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('seller-requests/', views.seller_requests, name='seller_requests'),
    path('seller-request/<int:seller_id>/', views.seller_request_detail, name='seller_request_detail'),
    path('sellers/', views.sellers_list, name='sellers-list'),
    path('seller/<int:seller_id>/', views.seller_view, name='seller_view'),
    path('buyers/', views.buyers_list, name='buyers-list'),
    path('sellers/toggle/<int:seller_id>/', views.toggle_seller_status, name='toggle-seller'),
    path('seller/reject/<int:seller_id>/', views.seller_reject_reason, name='seller_reject_reason'),


]
