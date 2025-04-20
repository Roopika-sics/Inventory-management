from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile', null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    business_address = models.TextField()
    registration_number = models.CharField(max_length=100)
    validation_document = models.FileField(upload_to='validation_documents/')
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name
