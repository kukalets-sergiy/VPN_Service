import os
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.http import  HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.views import View
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from vpn_service_core import settings
from vpn_service_core.extra_functions import reduce_image_size
from .forms import CustomUserCreationForm, ProfilePictureForm, SiteCreateForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import UserData, Site, ExternalLink, Statistics


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
    success_url = reverse_lazy("vpn_service_app:homepage")
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
            # Checks if the user with the specified name and password exists in the database
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

        # Get the user object by its email address
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
        name = request.POST.get("name").title()
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
            site = form.save()
            # Get or create a link to an external resource
            external_link, created = ExternalLink.objects.get_or_create(url=site.url)

        messages.success(request, "Data update completed successfully")
        return redirect("vpn_service_app:user-sites")

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
            proxy_url = reverse('vpn_service_app:proxy_view', args=(link.name, link.url.split('//')[-1]))
            # Append a tuple (link, proxy_url) to the proxy_urls list
            proxy_urls.append((link, proxy_url))
        # Render the template user_sites.html with the proxy_urls context variable
        return render(request, self.template_name, {"proxy_urls": proxy_urls})


class ExternalSiteFetcher:
    def __init__(self, url):
        self.url = url
    def fetch_html_content(self):
        try:
            #  Make a GET HTTP request to the specified URL
            response = requests.get(self.url)
            # Check if the response from the server was received successfully
            if response.status_code == 200:
                # Get the HTML code of the page and return it
                return response.text
            else:
                print("Unable to retrieve page content. Status code:", response.status_code)
                return None
        except Exception as e:
            print("An error occurred while executing the request:", e)
            return None


class ExternalSiteFetcherLink:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_html_content_link(self, proxy_link):
        try:
            # Combine the base URL with the page URL
            url = self.base_url + proxy_link
            # Make a GET HTTP request to the specified URL
            response = requests.get(url)
            # Check if the response from the server was received successfully
            if response.status_code == 200:
                # Get the HTML code of the page and return it
                return response.text
            else:
                print("Unable to retrieve page content. Status code:", response.status_code)
                return None
        except Exception as e:
            print("An error occurred while executing the request:", e)
            return None


class LinkReplacer:
    def __init__(self, html_content, vpn_route, site_name, site_url):
        # Initialize LinkReplacer with HTML content, VPN route, site name, and site URL
        self.html_content = html_content
        self.vpn_route = vpn_route
        self.site_name = site_name
        self.site_url = site_url

    def replace_links(self):
        try:
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(self.html_content, 'html.parser')
            # Find all <a> tags with href attribute
            external_links = soup.find_all('a', href=True)
            # Iterate through each link found in the HTML content
            for link in external_links:
                # Check if the link starts with 'http://' or 'https://'
                if link['href'].startswith('http://') or link['href'].startswith('https://'):
                    # Replace the link with VPN route, site name, site URL, and link URL
                    link['href'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}/{link['href'].split('//')[-1]}"
                # Check if the link starts with '/'
                if link['href'].startswith('/'):
                    # Replace the link with VPN route, site name, site URL and link URL
                    link['href'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}{link['href']}"

            # external_css_links = soup.find_all('link', href=True)
            # for css_link in external_css_links:
            #     if css_link['href'].startswith('http://') or css_link['href'].startswith('https://'):
            #         css_link[
            #             'href'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}{css_link['href'].split('//')[-1]}"
            #     if css_link['href'].startswith('/'):
            #         css_link[
            #             'href'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}{css_link['href']}"

            external_js_links = soup.find_all('script', src=True)
            for js_link in external_js_links:
                if js_link['src'].startswith('http://') or js_link['src'].startswith('https://'):
                    js_link[
                        'src'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}/{js_link['src'].split('//')[-1]}"
                if js_link['src'].startswith('/'):
                    js_link[
                        'src'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}{js_link['src']}"

            external_img_links = soup.find_all('img', src=True)
            for img_link in external_img_links:
                if img_link['src'].startswith('http://') or img_link['src'].startswith('https://'):
                    img_link[
                        'src'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}/{img_link['src'].split('//')[-1]}"
                if img_link['src'].startswith('/'):
                    img_link[
                        'src'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}{img_link['src']}"

            external_meta_links = soup.find_all('meta', content=True)
            for meta_link in external_meta_links:
                if meta_link['content'].startswith('http://') or meta_link['content'].startswith('https://'):
                    meta_link[
                        'content'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}/{meta_link['content'].split('//')[-1]}"
                if meta_link['content'].startswith('/'):
                    meta_link[
                        'content'] = f"{self.vpn_route}/{self.site_name}/{self.site_url.split('//')[-1]}{meta_link['content']}"
            # Return the modified HTML content after link replacement
            return str(soup)
        # Handle any exceptions that occur during link replacement
        except Exception as e:
            print("An error occurred while replacing links:", e)
            # Return None if an error occurs
            return None


class ProxyView(View):
    def get(self, request, user_site_name, routes_on_original_site):
        try:
            # Get the site object based on the user_site_name from the database
            site = get_object_or_404(Site, name=user_site_name)

            # Extract the path part of the site URL
            link_path = site.url.split('//')[-1].rstrip('/')
            link_path_slash = site.url.split('//')[-1]

            # Extract the proxy link from the request's full path
            proxy_link = request.get_full_path().split(link_path_slash)[-1]

            # Fetch the HTML content of the original site
            external_site_fetcher = ExternalSiteFetcher(site.url)
            html_content = external_site_fetcher.fetch_html_content()

            if html_content:
                # Replace links in the HTML content with the proxy route
                link_replacer = LinkReplacer(html_content, "http://localhost:8000", user_site_name, link_path)
                updated_html_content = link_replacer.replace_links()

                # Check if the proxy link is in the updated HTML content
                if proxy_link in updated_html_content:
                    # Fetch HTML content for the proxy link
                    external_site_fetcher_link = ExternalSiteFetcherLink(site.url)
                    html_content_link = external_site_fetcher_link.fetch_html_content_link(proxy_link)

                    if html_content_link:
                        # Replace links in the HTML content for the proxy link
                        link_replacer_link = LinkReplacer(html_content_link, "http://localhost:8000",
                                                          user_site_name, link_path)
                        updated_html_content_link = link_replacer_link.replace_links()

                        try:
                            # Update statistics for the user and site
                            statistics_obj = Statistics.objects.get(user=request.user, site=site)
                            # Update the values
                            statistics_obj.page_views += 1
                            data_sent_bytes = len(html_content_link.encode('utf-8'))
                            data_received_bytes = len(updated_html_content_link.encode('utf-8'))
                            statistics_obj.data_sent += data_sent_bytes
                            statistics_obj.data_received += data_received_bytes
                            statistics_obj.save()
                        except Statistics.DoesNotExist:
                            # Create a new record if it does not exist
                            statistics_obj = Statistics.objects.create(
                                user=request.user,
                                site=site,
                                page_views=1,
                                data_sent=len(html_content_link.encode('utf-8')),
                                data_received=len(updated_html_content_link.encode('utf-8'))
                            )

                        return HttpResponse(updated_html_content_link, content_type='text/html')
                    else:
                        return HttpResponse(updated_html_content, content_type='text/html')

                return HttpResponse(updated_html_content, content_type='text/html')
            else:
                return HttpResponseNotFound('Page not found')

        except Site.DoesNotExist:
            return HttpResponseNotFound('Site not found')
        except Exception as e:
            print(f'Error: {e}')
            return HttpResponseServerError('An error occurred')


class StatisticsView(View):
    template_name = 'statistics.html'
    def get(self, request):
        statistics = Statistics.objects.all()
        # Passing data to the template for display
        return render(request, 'statistics.html', {'statistics': statistics})
