from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from books.models import Book, Follow
from users.serializers import UserSerializer
from taskScheduling.send import sendEmailFollowBookUser
import threading

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
            "follows"
        ]
        read_only_fields = ["id", "copies"]
        extra_kwargs = {
            "name": {
                "validators": [
                    UniqueValidator(
                        queryset=Book.objects.all(),
                        message="This book already exists.",
                    )
                ]
            },
        }

        def create(self, validated_data):
            return Book.objects.create(**validated_data)

        def update(self, instance: Book, validated_data: dict) -> Book:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()
            return instance


class FollowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "date", "book", "user"]
        read_only_fields = ["id", "date", "book", "user"]

    def create(self, validated_data):

        book = validated_data["book"]
        user = validated_data["user"]

        following = Follow.objects.filter(book_id=book.id, user_id=user.id).first()

        if not following:
            following = Follow.objects.create(**validated_data)
            email = threading.Thread(target=sendEmailFollowBookUser, args=(validated_data, 5))
            email.start()
        
        return following
