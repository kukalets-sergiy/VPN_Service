from django import forms
from .models import UserData, Site
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserData
        fields = ('username', 'email', 'password1', 'password2')


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

    def __init__(self, *args, **kwargs):
        super(SiteCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["url"].required = False


