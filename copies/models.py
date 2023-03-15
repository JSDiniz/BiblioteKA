import uuid
import ipdb
from django.db import models


class Copy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_avaliable = models.BooleanField(default=True)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )

    borrowers = models.ManyToManyField(
        "users.User", through="copies.Loan", related_name="books_copies"
    )


class Loan(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    lend_at = models.DateField(auto_now_add=True)
    refund_at = models.DateField(null=True)

    book_copy = models.ForeignKey(
        "copies.Copy",
        on_delete=models.SET_NULL,
        related_name="copy_loans",
        null=True,
    )

    borrower = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_loans",
    )
