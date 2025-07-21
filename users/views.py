"""Views for user authentication via HTMX."""

from django.shortcuts import redirect, render
from django.views import View
from users.forms import LoginForm
from users.services.auth import login_user


class LoginView(View):
    """Render and handle the login form."""

    def get(self, request):
        """Display the login page."""
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        """Process login submissions."""
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if login_user(request, email, password):
                return redirect("/")  # replace later with actual homepage
        return render(
            request,
            "users/login.html",
            {"form": form, "error": "Invalid credentials"},
        )
