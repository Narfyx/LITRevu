from django.db import models


class Utilisateur(models.Model):
    nom_utilisateur = models.CharField(max_length=20)
    mot_de_passe = models.CharField(max_length=64)
