# Generated by Django 5.0.4 on 2024-05-15 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("actions_users", "0007_review_body_review_headline"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="title",
        ),
    ]
