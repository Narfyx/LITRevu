# Generated by Django 5.0.4 on 2024-05-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("actions_users", "0009_remove_review_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]