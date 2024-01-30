from django.contrib import admin
from vpn_service_app.views import (
    HomePageView,
    RegistrationView,
    LoginView,
    LogoutView,
)

from django.urls import path

app_name = "vpn_service_app"

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]

app_name = "vpn_service_app"
