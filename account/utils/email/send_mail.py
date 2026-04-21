# Send otp mail to user for acount validation
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from account.models import CustomUser

# OTP MAIL SENDER
def send_otp_email(user, otp):
    subject = "Verify your email"
    html_content = render_to_string(
        "emails/email_otp_verification.html",
        {"user": user, "otp": otp}
    )

    email = EmailMultiAlternatives(
        subject,
        to=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def notify_admins_new_user(user):
    admins = CustomUser.objects.filter(role="admin", is_active=True)
    emails = [admin.email for admin in admins]

    # Send email to admins using the email html template
    subject = "New User Registration Awaiting Approval"
    html_content = render_to_string(
        "emails/email_admin_pending_approval.html",
        {"user": user,}
    )
    email = EmailMultiAlternatives(
        subject,
        to=emails,
        from_email=settings.DEFAULT_FROM_EMAIL
    )
    email.attach_alternative(html_content, "text/html")
    email.send()