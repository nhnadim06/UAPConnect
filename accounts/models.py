import uuid
from datetime import datetime, timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from common.models import BaseModel

from .manager import CustomUserManager

# How long a verification code or reset token stays valid, in seconds.
CODE_EXPIRY_SECONDS = 20 * 60


class TokenType(models.TextChoices):
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"


class TimeLimitedMixin(models.Model):
    """
    Shared expiry logic for any model that needs to be treated as
    'stale' after a fixed window (verification codes, reset tokens, etc).
    """

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @property
    def is_expired(self) -> bool:
        age = datetime.now(timezone.utc) - self.created_at
        return age.total_seconds() > CODE_EXPIRY_SECONDS

    def is_valid(self) -> bool:
        # Kept for backwards-compatible call sites; prefer is_expired.
        return not self.is_expired


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UnverifiedRegistration(BaseModel, TimeLimitedMixin):
    """
    Holds a signup attempt until the user confirms it via the emailed
    verification code. Promoted to a real User once confirmed.
    """

    email = models.EmailField()
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)

    def __str__(self):
        return f"pending signup: {self.email}"


class AuthToken(TimeLimitedMixin):
    """
    Short-lived token used for flows like password reset.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices=TokenType.choices)

    def __str__(self):
        return f"{self.user} :: {self.token_type}"

    def reset_user_password(self, raw_password: str):
        self.user.set_password(raw_password)
        self.user.save()
