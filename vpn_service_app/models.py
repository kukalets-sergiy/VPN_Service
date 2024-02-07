from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models

from vpn_service_core import settings


class UserData(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

"""
Site: A model for storing information about sites created by users, including URL and name.

Statistics: A model for storing user activity statistics, including the number of page views, and the amount of data sent and downloaded for each site.

ExternalLink: A model for storing external links.

"""


class Site(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name

class Statistics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0)
    data_sent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class ExternalLink(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url
