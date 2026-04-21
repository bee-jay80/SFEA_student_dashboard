from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class OTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.CharField(max_length=256)  # Increased to accommodate hashed OTP codes (~80-256 chars)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"
    
