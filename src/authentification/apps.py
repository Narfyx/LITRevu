"""
App configuration for the authentification app.
"""

from django.apps import AppConfig


class AuthentificationConfig(AppConfig):
    """
    Configuration class for the authentification app.

    Attributes:
        default_auto_field (str): Specifies the default auto field type.
        name (str): The name of the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentification"
