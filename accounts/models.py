# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True)
    blood_group = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)

    def __str__(self):
        return self.user.username
