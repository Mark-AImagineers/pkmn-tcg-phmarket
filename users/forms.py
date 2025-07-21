from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "autocomplete": "email",
                "id": "id_email",
                "placeholder": "Email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "current-password",
                "id": "id_password",
                "placeholder": "Password",
            }
        )
    )
