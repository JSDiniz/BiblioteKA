from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    copies = serializers.IntegerField(source="copies.count", read_only=True)

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
            "copies",
        ]
        read_only_fields = ["id", "copies"]

        def create(self, validated_data):
            return Book.objects.create(**validated_data)

        def update(self, instance: Book, validated_data: dict) -> Book:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()
            return instance
