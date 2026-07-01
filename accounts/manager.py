from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """
    Manager for the custom User model, using email instead of
    username as the unique login identifier.
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValidationError("An email address is required to create a user.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValidationError("Superuser accounts must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValidationError("Superuser accounts must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
