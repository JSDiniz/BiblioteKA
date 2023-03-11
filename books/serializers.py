from rest_framework import serializers

from books.models import Book, Follow


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

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = [
            "id",
            "date",
            "book",
            "user"
        ]
        read_only_fields = ["date", "book", "user"]

    def create(self, validated_data):
        book = validated_data["book"]
        user = validated_data["user"]
        
        following = Follow.objects.filter(book_id=book.id).filter(user_id=user.id).first()
        
        if following:      
            ...
                    
        return Follow.objects.create(**validated_data)