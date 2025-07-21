"""Forms used across the users app."""

from django import forms


class LoginForm(forms.Form):
    """Simple login form with Tailwind CSS styling."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 rounded bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-green-400"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 rounded bg-white/10 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-green-400"
            }
        )
    )
