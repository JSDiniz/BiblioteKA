import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_employee = models.BooleanField(default=False, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

