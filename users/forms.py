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


class RegisterForm(forms.Form):
    """Form for user registration."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "autocomplete": "email",
                "id": "id_reg_email",
                "placeholder": "Email",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "id": "id_password1",
                "placeholder": "Password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "id": "id_password2",
                "placeholder": "Confirm Password",
            }
        )
    )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class PasswordResetRequestForm(forms.Form):
    """Simple form to request a password reset email."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "autocomplete": "email",
                "id": "id_reset_email",
                "placeholder": "Email",
            }
        )
    )


class SetNewPasswordForm(forms.Form):
    """Form for setting a new password during reset."""

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "id": "id_new_password1",
                "placeholder": "New Password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "autocomplete": "new-password",
                "id": "id_new_password2",
                "placeholder": "Confirm Password",
            }
        )
    )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
