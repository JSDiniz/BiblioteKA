# Generated by Django 4.1.7 on 2023-03-10 18:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="is_available",
        ),
    ]
