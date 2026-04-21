from account.otp_models import OTP
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

def verify_otp(user, submitted_otp):
    try:
        otp_instance = OTP.objects.filter(user=user).latest('created_at')
    except OTP.DoesNotExist:
        return False, "OTP not found"

    if otp_instance.is_expired():
        # delete the expired OTP instance
        otp_instance.delete()
        return False, "OTP expired"

    if not check_password(submitted_otp, otp_instance.code):
        return False, "Invalid OTP"

    return True, "OTP verified"