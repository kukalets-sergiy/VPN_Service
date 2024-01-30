from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.views import View, generic
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm


class HomePageView(generic.TemplateView):
    template_name = "homepage.html"


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
