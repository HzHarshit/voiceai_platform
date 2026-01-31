from django.db import models
from django.contrib.auth.models import AbstractUser
from tenants.models import Tenant


class User(AbstractUser):
    email = models.EmailField(unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
