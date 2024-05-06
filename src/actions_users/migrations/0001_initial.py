# Generated by Django 5.0.4 on 2024-04-30 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authentification", "0002_alter_utilisateur_mot_de_passe_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserFollows",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "followed_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to="authentification.utilisateur",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to="authentification.utilisateur",
                    ),
                ),
            ],
            options={
                "ordering": ["user__nom_utilisateur"],
                "unique_together": {("user", "followed_user")},
            },
        ),
    ]