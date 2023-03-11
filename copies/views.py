import ipdb
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from books.serializers import BookSerializer
from users.models import User
from users.permission import IsAdminOrOwner

from .models import Copy
from .serializers import CopySerializer, LoanSerializer
from emailsSend.send import sendEmailCopyBook


class CopyView(generics.CreateAPIView):
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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"datail": "quantity field is missing"}, status=status.HTTP_400_BAD_REQUEST
        )


class ListCopiesView(generics.ListAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class LoanView(generics.CreateAPIView):
    def post(self, request: Request, copy_id, user_id):
        copy = get_object_or_404(Copy, id=copy_id)
        user = get_object_or_404(User, id=user_id)

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
