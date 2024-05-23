"""
Models for user relationships, tickets, and reviews.
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserFollows(models.Model):
    """
    Model representing the relationship where a user follows another user.

    Attributes:
        user (ForeignKey): The user who is following.
        followed_user (ForeignKey): The user who is being followed.
    """

    # L'utilisateur qui suit
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,  # Référence au modèle utilisateur personnalisé
        related_name="following",  # Facilite l'accès aux utilisateurs suivis par cet utilisateur
        # Si l'utilisateur est supprimé, ses relations de suivi sont également supprimées
        on_delete=models.CASCADE,
    )
    # L'utilisateur qui est suivi
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        # Assure que chaque paire utilisateur-utilisateur suivi est unique
        unique_together = ("user", "followed_user")
        # correction bug dans l'interface django admin pour corriger le "User followss"
        verbose_name = "User follow"
        verbose_name_plural = "User follows"

    def __str__(self):
        # Représentation en chaîne de caractères de l'objet
        return f"{self.user.username} follows {self.followed_user.username}"


class BasePost(models.Model):
    """
    Abstract model for common fields in Ticket and Review models.

    Attributes:
        time_created (DateTimeField): The timestamp when the post was created.
        user (ForeignKey): The user who created the post.
    """

    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Ticket(BasePost):
    """
    Model representing a ticket.

    Attributes:
        title (CharField): The title of the ticket.
        description (TextField): The description of the ticket.
        image (ImageField): An optional image associated with the ticket.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(blank=True, null=True)


class Review(BasePost):
    """
    Model representing a review.

    Attributes:
        headline (CharField): The headline of the review.
        body (TextField): The body content of the review.
        ticket (ForeignKey): The ticket associated with the review.
        rating (PositiveSmallIntegerField): The rating given in the review, between 0 and 5.
    """

    headline = models.CharField(max_length=128, null=True, blank=True)
    body = models.TextField(
        max_length=8192, null=True, blank=True
    )  # Body peut être vide

    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE
    )  # Lien vers le ticket associé
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    # Note attribuée, entre 0 et 5
