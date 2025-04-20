from django.db import models
from django.conf import settings
from categories.models import Category
# Create your models here.
# products/models.py


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    brand_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def final_price(self):
        return self.base_price - self.discount

    def saved_amount(self):
        return self.discount

    def discount_percentage(self):
        if self.base_price > 0:
            return (self.discount / self.base_price) * 100
        return 0
