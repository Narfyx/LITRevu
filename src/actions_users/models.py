from django.conf import settings
#from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

from authentification.models import User


class UserFollows(models.Model):
    # L'utilisateur qui suit
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,  # Référence au modèle utilisateur personnalisé
        related_name="following",  # Facilite l'accès aux utilisateurs suivis par cet utilisateur
        on_delete=models.CASCADE,  # Si l'utilisateur est supprimé, ses relations de suivi sont également supprimées
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
        verbose_name = "User follow"  # correction bug dans l'interface django admin pour corriger le "User followss"
        verbose_name_plural = "User follows"  # correction bug dans l'interface django admin pour corriger le "User followss"

    def __str__(self):
        # Représentation en chaîne de caractères de l'objet
        return f"{self.user.username} follows {self.followed_user.username}"


class BasePost(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Ticket(BasePost):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(blank=True, null=True)


class Review(BasePost):
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
