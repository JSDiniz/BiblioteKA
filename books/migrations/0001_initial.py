# Generated by Django 4.1.7 on 2023-03-14 21:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("name", models.CharField(max_length=80, unique=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=120)),
                ("author", models.CharField(max_length=50)),
                ("category", models.CharField(max_length=20)),
                ("pages", models.PositiveIntegerField(default=0)),
                ("release_date", models.DateField()),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.UUIDField(
<<<<<<< HEAD
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
=======
                        default=uuid.uuid4, primary_key=True, serialize=False
>>>>>>> refactor/books_views
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="book_followers",
                        to="books.book",
                    ),
                ),
            ],
        ),
    ]
