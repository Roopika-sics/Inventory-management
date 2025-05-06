from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class DeliveryAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='delivery_agent_profile', null=True)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    licence_number = models.CharField(max_length=100)
    licence_expiry_date = models.DateField()
    driving_licence = models.ImageField(upload_to='driving_licences/')

    def __str__(self):
        return self.user.username