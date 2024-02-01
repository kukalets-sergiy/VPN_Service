import os

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.checks import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.views import View, generic
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework import request


from vpn_service_core import settings
from vpn_service_core.extra_functions import reduce_image_size
from .forms import CustomUserCreationForm, ProfilePictureForm, SiteCreateForm
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import UserData, Site


class HomePageView(View):
    template_name = "homepage.html"
    def get(self, request):
        if request.user.is_authenticated:
            user_obj = get_object_or_404(get_user_model(), email=request.user.email)
            return render(
                request,
                self.template_name,
                {"user": user_obj},)
        else:
            return redirect("vpn_service_app:login")


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration.html"


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            form = AuthenticationForm()
            return render(request, self.template_name, {"login_form": form})
        else:
            messages.info(request, f"You are already logged in as {user.email}.")
            return redirect("vpn_service_app:homepage")

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("vpn_service_app:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        return render(
            request,
            self.template_name,
            context={"login_form": form},
        )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("vpn_service_app:login")


class UploadProfilePictureView(View):
    template_name = "upload_profile_picture.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("vpn_service_app:login")

        user = get_object_or_404(get_user_model(), email=request.user.email)
        form = ProfilePictureForm(instance=user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user = request.user
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_data = get_object_or_404(UserData, email=request.user.email)

            # Build the full path to the picture file using the MEDIA_ROOT setting
            profile_picture_path = os.path.join(settings.MEDIA_ROOT, str(user_data.profile_picture))

            try:
                os.remove(profile_picture_path)
                print(f"File '{profile_picture_path}' successfully removed.")
                user_data.profile_picture = form.cleaned_data["profile_picture"]

                user_data.save()
                reduce_image_size(user_data.profile_picture)
                messages.success(request, "Profile picture updated successfully")
                return redirect("vpn_service_app:homepage")

            except:
                user_data.profile_picture = form.cleaned_data["profile_picture"]
                user_data.save()
                reduce_image_size(user_data.profile_picture)
                messages.success(request, "Profile picture uploaded successfully")
                return redirect("vpn_service_app:homepage")

        return render(request, self.template_name, {"form": form})


class DeleteProfilePictureView(View):
    def post(self, request):
        user = get_object_or_404(get_user_model(), email=request.user.email)

        # Build the full path to the picture file using the MEDIA_ROOT setting
        profile_picture_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture))
        user.profile_picture = None
        try:
            os.remove(profile_picture_path)
            print(f"File '{profile_picture_path}' successfully removed.")
        except Exception as e:
            print(f"Error removing file: {e}")
        # Save the model to update the database
        user.save()
        messages.success(request, "Profile picture removed successfully")
        return redirect("vpn_service_app:homepage")

class UserSitesView(View):
    template_name = "user_sites.html"

    def get(self, request):
        # Retrieve all Site objects from the database
        links = Site.objects.all()
        # Create an empty list to store pairs of (link, proxy_url)
        proxy_urls = []
        # Iterate through each link in the retrieved Site objects
        for link in links:
            # Generate the proxy_url using the reverse() function, passing link name and url as arguments
            proxy_url = reverse('vpn_service_app:proxy_view', args=(link.name, link.url))
            # Append a tuple (link, proxy_url) to the proxy_urls list
            proxy_urls.append((link, proxy_url))
        # Render the template user_sites.html with the proxy_urls context variable
        return render(request, self.template_name, {"proxy_urls": proxy_urls})


class SiteCreateView(View):
    template_name = "site_create.html"
    def get(self, request):
        form = SiteCreateForm()
        links = Site.objects.all()

        return render(request, self.template_name, {"form": form, "links": links})

    def post(self, request):
        form = SiteCreateForm(request.POST)

        links_to_remove = request.POST.getlist("links_to_remove")
        if links_to_remove:
            for link_id in links_to_remove:
                link = get_object_or_404(Site, id=link_id)
                link.delete()
        name = request.POST.get("name").capitalize()
        if name:
            if Site.objects.filter(name=name).exists():
                messages.error(request, "Such name already exist, try another name")
                return redirect("vpn_service_app:site_create")
        url = request.POST.get("url")
        if url:
            if Site.objects.filter(url=url).exists():
                messages.error(request, "Such syte already exist")
                return redirect("vpn_service_app:site_create")
        # Check that the fields are not empty
        if name and url:
            links = form.save()
            links.save()

        messages.success(request, "Data update completed successfully")
        return redirect("vpn_service_app:user-sites")


class ProxyView(View):
    def get(self, request, user_site_name, routes_on_original_site):
        try:
            # Try to retrieve the Site object with the given name from the database
            site = get_object_or_404(Site, name=user_site_name)
            # Extract the path from the site URL after the double slashes (//)
            link_path = site.url.rsplit("//", 1)[1]
            # Check if the site has an external URL specified
            if site.external_url:
                external_url = site.external_url
            else:
                # If not, construct the external URL using the localhost address and site name
                external_url = f"http://localhost:8000/{site.name}/{link_path}"
            # Redirect the user to the external URL
            return HttpResponseRedirect(external_url)
        except Site.DoesNotExist:
            # Return a 404 Not Found response if the site is not found in the database
            return HttpResponseNotFound('Site not found')
        except Exception as e:
            # Handle any other unexpected errors that may occur
            print(f'Error: {e}')
            return HttpResponseServerError('An error occurred')

