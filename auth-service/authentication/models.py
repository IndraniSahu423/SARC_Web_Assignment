from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, name, roll_number, hostel_number, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field is required.")
        if not roll_number:
            raise ValueError("The roll_number field is required.")
        if not password:
            raise ValueError("The password field is required.")

        user = self.model(
            username=username,
            name=name,
            roll_number=roll_number,
            hostel_number=hostel_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, roll_number, hostel_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username=username,
            name=name,
            roll_number=roll_number,
            hostel_number=hostel_number,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=50, unique=True)
    hostel_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "roll_number", "hostel_number"]

    def __str__(self):
        return f"{self.username} ({self.roll_number})"
