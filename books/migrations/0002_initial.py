# Generated by Django 4.1.7 on 2023-03-13 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="follow",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_follows",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="follows",
            field=models.ManyToManyField(
                related_name="book_follow",
                through="books.Follow",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
