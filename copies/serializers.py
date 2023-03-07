from copies.models import Copy, Loan
from rest_framework import serializers
from users.serializers import UserSerializer
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer()
    borrowers = UserSerializer(many=True)

    class Meta:
        model = Copy
        fields = [
            "id",
            "is_avaliable",
            "book"
            "borrowers"
        ]
        read_only_fields = ["id","borrowers"]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "lend_at",
            "refund_at",
            "expires_at",
            "book_copy",
            "borrower"
        ]
        read_only_fields = ["id"]