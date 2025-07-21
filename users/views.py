from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm, RegisterForm
from users.services.auth import login_user, register_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if login_user(request, email, password):
                return redirect("/")  # replace later with actual homepage
        return render(
            request, "users/login.html", {"form": form, "error": "Invalid credentials"}
        )


class RegisterView(View):
    """Display and process the user registration form."""

    def get(self, request):
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            register_user(form.cleaned_data["email"], form.cleaned_data["password1"])
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        for error in form.errors.values():
            messages.error(request, error)
        return render(request, "users/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display the logged-in user's profile."""

    template_name = "users/profile.html"
