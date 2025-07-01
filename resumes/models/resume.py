from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=200, null=True, blank=True
    )
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
