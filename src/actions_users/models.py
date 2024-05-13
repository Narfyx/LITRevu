from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

from authentification.models import Utilisateur


class UserFollows(models.Model):
    # L'utilisateur qui suit
    user = models.ForeignKey(
        User,  # Référence au modèle utilisateur personnalisé
        related_name="following",  # Facilite l'accès aux utilisateurs suivis par cet utilisateur
        on_delete=models.CASCADE,  # Si l'utilisateur est supprimé, ses relations de suivi sont également supprimées
    )
    # L'utilisateur qui est suivi
    followed_user = models.ForeignKey(
        User,  # Référence au même modèle utilisateur
        related_name="followers",  # Facilite l'accès aux utilisateurs qui suivent cet utilisateur
        on_delete=models.CASCADE,  # Si l'utilisateur suivi est supprimé, cette relation de suivi est également supprimée
    )

    class Meta:
        # Assure que chaque paire utilisateur-utilisateur suivi est unique
        unique_together = ("user", "followed_user")

    def __str__(self):
        # Représentation en chaîne de caractères de l'objet
        return f"{self.user.username} follows {self.followed_user.username}"


class Ticket(models.Model):

    IMAGE_MAX_SIZE = (2000, 2000)

    title = models.CharField(max_length=96)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def resize_image(self):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
