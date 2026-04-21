from django.contrib import admin
from .models import CustomUser, Profile
from .otp_models import OTP

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(OTP)