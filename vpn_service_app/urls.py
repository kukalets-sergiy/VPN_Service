from django.urls import path
from vpn_service_app.views import (
    HomePageView,
    RegistrationView,
    LoginView,
    LogoutView,
    UploadProfilePictureView,
    DeleteProfilePictureView,
    UserSitesView,
    SiteCreateView,
    ProxyView,
)


urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("upload-profile-picture/", UploadProfilePictureView.as_view(), name="upload_profile_picture"),
    path("delete-profile-picture/", DeleteProfilePictureView.as_view(), name="delete_profile_picture"),
    path("user-sites/", UserSitesView.as_view(), name="user-sites"),
    path("site-create/", SiteCreateView.as_view(), name="site_create"),
    path('proxy/<str:user_site_name>/<path:routes_on_original_site>/', ProxyView.as_view(), name='proxy_view'),
]

app_name = "vpn_service_app"
