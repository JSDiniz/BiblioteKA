from django.db import models
import uuid


class Book(models.Model):
    class Meta:
        ordering = ("name",)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=120, blank=True)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    pages = models.PositiveIntegerField(default=0)
    release_date = models.DateField()

    follows = models.ManyToManyField(
        "users.User",
        through="books.Follow",
        related_name="book_follow",
    )


class Follow(models.Model):
    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="book_followers",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE, 
        related_name="user_follows",
        default = None
    )

    date = models.DateTimeField(auto_now_add=True)
