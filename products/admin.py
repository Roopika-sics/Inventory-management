from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem, Review, ProductVariant, ProductAttributeValue, ProductAttribute
# Register your models here.

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(ProductVariant)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductAttribute)