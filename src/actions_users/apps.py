"""
App configuration for the actions_users app.
"""

from django.apps import AppConfig


class ActionsUsersConfig(AppConfig):
    """
    Configuration class for the actions_users app.

    Attributes:
        default_auto_field (str): Specifies the default auto field type.
        name (str): Name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "actions_users"
