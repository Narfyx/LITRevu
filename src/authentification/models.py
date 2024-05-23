"""
Models for user authentication and authorization.
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending the AbstractUser model.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        groups (ManyToManyField): The groups this user belongs to.
        user_permissions (ManyToManyField): Specific permissions for this user.
    """

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Nom de relation unique
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Nom de relation unique
        blank=True,
        help_text=("Specific permissions for this user."),
        related_query_name="user",
    )
