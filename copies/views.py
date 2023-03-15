import ipdb
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import  Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from users.models import User
from books.serializers import BookSerializer

from .models import Copy, Loan
from .serializers import CopySerializer, LoanSerializer
from emailsSend.send import sendEmailCopyBook
from .permissions import IsAdminOrLoanOwner
from django.db import connection

class CopyView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer


    def create(self, request, *args, **kwargs):
        found_book = get_object_or_404(Book, id=self.kwargs.get("pk"))
        quantity = self.request.data.get("quantity", None)
        if quantity:
            copies = [Copy(book=found_book) for _ in range(quantity)]

            copies = Copy.objects.bulk_create(copies)
            found_book.refresh_from_db()
            serializer = BookSerializer(found_book)

            sendEmailCopyBook(serializer.data)

            new_copies = Copy.objects.filter(id__in=[copy.id for copy in copies])
            new_copies_serializer = CopySerializer(new_copies, many=True)
            return Response(new_copies_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"datail": "quantity field is missing"}, status=status.HTTP_400_BAD_REQUEST
        )


class ListCopiesView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class LoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def post(self, request: Request, copy_id, user_id):
        copy = get_object_or_404(Copy, id=copy_id)
        user = get_object_or_404(User, id=user_id)

        if user.is_blocked == True:
            return Response(
                {"message": "This user is blocked"}, status.HTTP_404_NOT_FOUND
            )

        if not copy.is_avaliable:
            return Response(
                {"message": "This book is not available"}, status.HTTP_404_NOT_FOUND
            )

        serializer = LoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(book_copy=copy, borrower=user)

        copy.is_avaliable = False
        copy.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ListLoanView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        if self.request.user.is_employee:
            return Loan.objects.all()
        
        return Loan.objects.filter(
            borrower=self.request.user
        )
    


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrLoanOwner]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_update(self, serializer):
        serializer.save()

        
        loan = serializer.instance
        copy = loan.book_copy
        user = loan.borrower
        
        if not copy.is_avaliable and loan.refund_at > serializer.data["expires_at"]:
            now = timezone.now()
            blocked_until = now + timedelta(days=3)

            user.is_blocked = True
            user.blocked_until = blocked_until
            user.save()

        copy.is_avaliable = True
        copy.save()

