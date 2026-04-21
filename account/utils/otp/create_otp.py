import random
from account.otp_models import OTP
from django.contrib.auth.hashers import make_password

def create_otp(user):
    # Generate a random 6-digit OTP
    otp_code = str(random.randint(100000, 999999))

    # Hash the OTP code before saving to the database
    hashed_otp = make_password(otp_code)

    # Create and save the OTP instance
    otp_instance = OTP(user=user, code=hashed_otp)
    otp_instance.save()
    
    return otp_code  # Return the plain OTP code for sending to the user