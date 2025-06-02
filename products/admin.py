from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem, Review, ProductVariant, ProductAttributeValue, ProductAttribute, Invoice
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'seller', 'category']
    list_filter = ['status', 'category']
    search_fields = ['name', 'brand_name', 'model_number']
    
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(ProductVariant)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Invoice)