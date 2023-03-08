from books.models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "description",
            "author",
            "category",
            "pages",
            "release_date",
        ]
        read_only_fields = ["id"]
