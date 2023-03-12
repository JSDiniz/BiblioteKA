from datetime import date, timedelta

from rest_framework import serializers

from books.serializers import BookSerializer
from copies.models import Copy, Loan
from users.serializers import UserSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer()
    borrowers = UserSerializer(many=True)

    class Meta:
        model = Copy
        fields = ["id", "is_avaliable", "book", "borrowers"]
        read_only_fields = ["id", "book", "borrowers"]


class LoanSerializer(serializers.ModelSerializer):
    expires_at = serializers.SerializerMethodField()
    borrower = serializers.SerializerMethodField()
    book_name = serializers.SerializerMethodField()
    
    def get_expires_at(self, obj: Loan):
        expiration = obj.lend_at + timedelta(days=7)
        return expiration


    def get_borrower(self, obj: Loan):
        return obj.borrower.email
    

    def get_book_name(self, obj: Loan):
        if obj.book_copy:
            return obj.book_copy.book.name
        return None
    

    class Meta:
        model = Loan
        fields = [
            "id",
            "lend_at",
            "refund_at",
            "expires_at",
            "book_copy",
            "book_name",
            "borrower",
        ]
        read_only_fields = ["id", "book_copy", "borrower"]

        def create(self, validated_data: dict) -> Loan:
            return Loan.objects.create(**validated_data)
