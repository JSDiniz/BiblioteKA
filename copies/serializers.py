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


"""
1 encontrar o livro 
2 encontrar o user 
"""


class LoanSerializer(serializers.ModelSerializer):
    expires_at = serializers.SerializerMethodField()

    # borrower = serializers.CharField(source="users.username")
    def get_expires_at(self, obj: Loan):
        expiration = obj.lend_at + timedelta(days=7)
        return expiration

    class Meta:
        model = Loan
        fields = [
            "id",
            "lend_at",
            "refund_at",
            "expires_at",
            "book_copy",
            "borrower",
        ]
        read_only_fields = ["id", "book_copy", "borrower"]

        def create(self, validated_data: dict) -> Loan:
            return Loan.objects.create(**validated_data)
