from datetime import datetime, timezone

from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from .decorators import redirect_authenticated_user
from .models import AuthToken, TokenType, UnverifiedRegistration, User

NOREPLY_ADDRESS = "noreply@uapconnect.local"


def home(request):
    return render(request, "home.html")


# -------------------- Login -------------------- #
@redirect_authenticated_user
def login(request: HttpRequest):
    if request.method != "POST":
        return render(request, "login.html")

    email = request.POST.get("email")
    password = request.POST.get("password")
    user = auth.authenticate(request, email=email, password=password)

    if user is None:
        messages.error(request, "Invalid credentials.")
        return redirect("login")

    auth.login(request, user)
    messages.success(request, "You are now logged in.")
    return redirect("home")


# -------------------- Logout -------------------- #
def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, "You are now logged out.")
    return redirect("home")


# -------------------- Register -------------------- #
@redirect_authenticated_user
def register(request: HttpRequest):
    if request.method != "POST":
        return render(request, "register.html")

    email = request.POST["email"].lower()
    password = request.POST["password"]

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email exists on the platform.")
        return redirect("register")

    verification_code = get_random_string(10)

    UnverifiedRegistration.objects.update_or_create(
        email=email,
        defaults={
            "password": make_password(password),
            "verification_code": verification_code,
        },
    )

    _send_email(
        to=email,
        subject="Verify Your Account",
        body=f"Your verification code is: {verification_code}",
    )

    messages.success(request, f"Verification code sent to {email}")
    return render(request, "verify_account.html", {"email": email})


# -------------------- Verify Account -------------------- #
def verify_account(request: HttpRequest):
    if request.method != "POST":
        return redirect("register")

    code = request.POST["code"]
    email = request.POST["email"]

    pending = UnverifiedRegistration.objects.filter(
        verification_code=code, email=email
    ).first()

    if not pending or pending.is_expired:
        messages.error(request, "Invalid or expired verification code.")
        return render(request, "verify_account.html", {"email": email}, status=400)

    user = User.objects.create(email=pending.email)
    user.password = pending.password  # already hashed
    user.save()
    pending.delete()

    auth.login(request, user)
    messages.success(request, "Account verified. You are now logged in.")
    return redirect("home")


# -------------------- Forgot Password -------------------- #
def send_password_reset_link(request: HttpRequest):
    if request.method != "POST":
        return render(request, "forgot_password.html")

    email = request.POST.get("email", "").lower()
    user = get_user_model().objects.filter(email=email).first()

    if not user:
        messages.error(request, "Email not found")
        return redirect("reset_password_via_email")

    reset_token, _ = AuthToken.objects.update_or_create(
        user=user,
        token_type=TokenType.PASSWORD_RESET,
        defaults={
            "token": get_random_string(20),
            "created_at": datetime.now(timezone.utc),
        },
    )

    reset_link = (
        f"http://127.0.0.1:8000/auth/reset-password-confirm/"
        f"?email={email}&token={reset_token.token}"
    )

    _send_email(
        to=email,
        subject="Your Password Reset Link",
        body=f"Click the link below to reset your password:\n{reset_link}",
    )

    messages.success(request, "Reset link sent to your email")
    return redirect("reset_password_via_email")


# -------------------- Verify Password Reset Link -------------------- #
def verify_password_reset_link(request: HttpRequest):
    email = request.GET.get("email")
    token_value = request.GET.get("token")

    reset_token = AuthToken.objects.filter(
        user__email=email,
        token=token_value,
        token_type=TokenType.PASSWORD_RESET,
    ).first()

    if not reset_token or reset_token.is_expired:
        messages.error(request, "Invalid or expired reset link.")
        return redirect("reset_password_via_email")

    return render(
        request,
        "set_new_password_using_reset_token.html",
        {"email": email, "token": token_value},
    )


def set_new_password(request: HttpRequest):
    """Handles the POST from the reset form: email, token, password1, password2."""
    if request.method != "POST":
        return redirect("reset_password_via_email")

    email = request.POST.get("email")
    token_value = request.POST.get("token")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if not (email and token_value):
        messages.error(request, "Invalid request. Missing email or token.")
        return redirect("reset_password_via_email")

    if not password1 or not password2:
        messages.error(request, "Both password fields are required.")
        return render(
            request,
            "set_new_password_using_reset_token.html",
            {"email": email, "token": token_value},
            status=400,
        )

    if password1 != password2:
        messages.error(request, "Passwords do not match.")
        return render(
            request,
            "set_new_password_using_reset_token.html",
            {"email": email, "token": token_value},
            status=400,
        )

    reset_token = AuthToken.objects.filter(
        token=token_value,
        user__email=email,
        token_type=TokenType.PASSWORD_RESET,
    ).first()

    if not reset_token:
        messages.error(request, "Expired or Invalid reset link")
        return redirect("reset_password_via_email")

    if reset_token.is_expired:
        messages.error(request, "Expired or Invalid reset link")
        return redirect("reset_password_via_email")

    reset_token.reset_user_password(password1)
    reset_token.delete()

    messages.success(request, "Password changed.")
    return redirect("login")


# -------------------- Helpers -------------------- #
def _send_email(to: str, subject: str, body: str):
    send_mail(subject, body, NOREPLY_ADDRESS, [to])
