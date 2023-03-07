from django.db import models
import uuid

# Create your models here.


class Book(models.Model):
    class Meta:
        ordering = ["name"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=120, blank=True)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    pages = models.PositiveIntegerField(default=0)
    release_date = models.DateField()


class Follow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")
    date = models.DateTimeField(auto_now_add=True)
