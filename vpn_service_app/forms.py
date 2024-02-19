from django import forms
from .models import UserData, Site
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form to handle user registration.
    """
    class Meta:
        model = UserData
        fields = ("username", "email", "password1", "password2")  # Include password fields for user registration


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form to handle user profile updates.
    """
    class Meta:
        model = UserData
        fields = ("username", "email")  # Allow users to change their username and email only


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ("profile_picture",)


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "url"]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.title()
        return name


