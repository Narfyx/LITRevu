# Generated by Django 5.0.4 on 2024-05-15 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("actions_users", "0008_remove_review_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="description",
        ),
    ]
