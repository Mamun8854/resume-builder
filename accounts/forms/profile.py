# accounts/forms.py
from django import forms
from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_image', 'blood_group']
