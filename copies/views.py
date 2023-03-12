import ipdb
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from books.serializers import BookSerializer
from users.models import User
from users.permission import IsAdminOrOwner

from .models import Copy, Loan
from .serializers import CopySerializer, LoanSerializer
from .permissions import IsAdminOrLoanOwner


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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        if not copy.is_available:
            return Response(
                {"message": "This book is not available"}, status.HTTP_404_NOT_FOUND
            )

        serializer = LoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(book_copy=copy, borrower=user)

        copy.is_available = False
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
        copia = serializer.data["book_copy"]
        copia = Copy.objects.get(id=copia)
        copia.is_avaliable = True
        copia.save()
        
class LoanDetailView(generics.RetrieveUpdateAPIView):
    queryset = Loan
    serializer_class = LoanSerializer
    lookup_url_kwarg = "user_id"


