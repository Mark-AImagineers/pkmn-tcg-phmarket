"""HTMX compatible views for the users app."""

from django.shortcuts import render
from django.views.generic import TemplateView

from users.forms import (
    LoginForm,
    PasswordResetRequestForm,
    RegisterForm,
    SetNewPasswordForm,
)


class LoginView(TemplateView):
    """Render the login page. Authentication handled via API."""

    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context


class RegisterView(TemplateView):
    """Render the registration page. Uses API endpoint for creation."""

    template_name = "users/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RegisterForm()
        return context


class ProfileView(TemplateView):
    """User profile page. Data is fetched via the `/api/me/` endpoint."""

    template_name = "users/profile.html"


class PasswordResetRequestView(TemplateView):
    """Page to request a password reset link."""

    template_name = "users/password_reset_request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PasswordResetRequestForm()
        return context


class PasswordResetConfirmView(TemplateView):
    """Page for setting a new password via a reset link."""

    template_name = "users/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SetNewPasswordForm()
        return context
