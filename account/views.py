from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from account.utils.email.send_mail import send_otp_email, notify_admins_new_user
from account.utils.otp.create_otp import create_otp
from account.utils.otp.verify_otp import verify_otp
from account.utils.create_token import create_verification_token, verify_verification_token
from django.http import JsonResponse

# message
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        email = form.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if user and user.is_otp_verified:
                messages.info(request, 'An account with this email already exists. Please log in.')
                return redirect('login')
            elif user and not user.is_otp_verified:
                otp_code = create_otp(user)
                send_otp_email(user, otp_code)
                session_token = create_verification_token(user.id)
                # set cookie for OTP verification session on the redirect response
                messages.info(request, 'An OTP has been sent to your email for verification. Please check your inbox.')
                response = redirect('otp_verification')
                # cookie expires in 10 minutes (600 seconds)
                response.set_cookie(
                    key="otp_session_token",
                    value=session_token,
                    httponly=True,
                    samesite="None",
                    max_age=900,  # 15 mins
                    secure=True,
                )
                return response
        except CustomUser.DoesNotExist:
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False  # Deactivate account until it is verified
                user.save()
                otp_code = create_otp(user)
                send_otp_email(user, otp_code)
                session_token = create_verification_token(user.id)
                messages.success(request, 'Registration successful! An OTP has been sent to your email for verification. Please check your inbox.')
                response = redirect('otp_verification')
                response.set_cookie(
                    key="otp_session_token",
                    value=session_token,
                    httponly=True,
                    samesite="None",
                    max_age=900,  # 15 mins
                    secure=True,
                )                
                return response
    else:
        form = CustomUserCreationForm()
    return render(request, 'extends/auth/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
            if user and user.is_otp_verified:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid email or password.')
            elif user and not user.is_otp_verified:
                otp_code = create_otp(user)
                send_otp_email(user, otp_code)
                messages.info(request, 'Your account is not verified. An OTP has been sent to your email for verification. Please check your inbox.')
                response =  redirect('otp_verification')
                session_token = create_verification_token(user.id)
                response.set_cookie(
                    key="otp_session_token",
                    value=session_token,
                    httponly=True,
                    samesite="None",
                    max_age=900,  # 15 mins
                    secure=True,
                )

                return response
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email. Please register first.')
    return render(request, 'extends/auth/login.html')

def verify_otp_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        session_token = request.COOKIES.get('otp_session_token')

        if not session_token:
            messages.error(request, 'Verification session not found. Please register again.')
            return redirect('register')

        try:
            payload = verify_verification_token(session_token)
            if not payload:
                raise ValueError('invalid token')
            user_id = payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            # verify_otp returns (success: bool, message: str)
            result, message_text = verify_otp(user, otp)
            if result:
                user.is_otp_verified = True
                user.save()
                notify_admins_new_user(user)
                messages.success(request, 'Email verified successfully! Your account is now pending approval by an admin.')
                # clear the otp session cookie and send user to awaiting approval page
                response = redirect('awaiting_approval')
                response.delete_cookie('otp_session_token')
                return response
            else:
                messages.error(request, message_text)
        except Exception:
            messages.error(request, 'Invalid or expired verification session. Please register again.')
            return redirect('register')
    return render(request, 'extends/auth/verify_otp.html')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'extends/pages/profile.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def resend_otp_api(request):
    if request.method == 'POST':
        session_token = request.COOKIES.get('otp_session_token')

        if not session_token:
            return JsonResponse({'error': 'Verification session not found. Please register again.'}, status=400)

        try:
            payload = verify_verification_token(session_token)
            if not payload:
                return JsonResponse({'error': 'Invalid or expired verification session. Please register again.'}, status=400)
            user_id = payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            otp_code = create_otp(user)
            send_otp_email(user, otp_code)
            return JsonResponse({'message': 'OTP resent successfully.'})
        except Exception:
            return JsonResponse({'error': 'Invalid or expired verification session. Please register again.'}, status=400)

def awaiting_approval(request):
    return render(request, 'extends/auth/awaiting_approval.html')