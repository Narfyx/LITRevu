"""
Forms for user creation and authentication.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and passwords.

    Attributes:
        password1 (CharField): The first password input field.
        password2 (CharField): The second password input field for confirmation.
    """

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta(UserCreationForm.Meta):
        """
        Meta class to extend the UserCreationForm.Meta fields.
        """

        fields = UserCreationForm.Meta.fields + ("password1", "password2")
