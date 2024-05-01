from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from authentification.models import Utilisateur
from django.contrib.auth.models import User





class UserFollows(models.Model):
    # L'utilisateur qui suit
    user = models.ForeignKey(

        User,  # Référence au modèle utilisateur personnalisé
        
        related_name='following',  # Facilite l'accès aux utilisateurs suivis par cet utilisateur
        on_delete=models.CASCADE  # Si l'utilisateur est supprimé, ses relations de suivi sont également supprimées
    )
    # L'utilisateur qui est suivi
    followed_user = models.ForeignKey(

        User,  # Référence au même modèle utilisateur
        
        related_name='followers',  # Facilite l'accès aux utilisateurs qui suivent cet utilisateur
        on_delete=models.CASCADE  # Si l'utilisateur suivi est supprimé, cette relation de suivi est également supprimée
    )

    class Meta:
        # Assure que chaque paire utilisateur-utilisateur suivi est unique
        unique_together = ('user', 'followed_user')


    def __str__(self):
        # Représentation en chaîne de caractères de l'objet
        return f"{self.user.username} follows {self.followed_user.username}"


