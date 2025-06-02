from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile', null=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username