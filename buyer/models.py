from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile', null=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.street_address}, {self.city}"