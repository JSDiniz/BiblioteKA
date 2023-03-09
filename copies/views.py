from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from users.permission import IsAdminOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status

from .models import Copy
from .serializers import CopySerializer
from books.models import Book
from books.serializers import BookSerializer


class CopyView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        found_book = get_object_or_404(Book, id=self.kwargs.get("pk"))
        quantity = self.request.data.get("quantity", None)
        if quantity:
            copies = [
                Copy(book = found_book)
                for _ in range(quantity)
            ]

            copies = Copy.objects.bulk_create(copies)
            found_book.refresh_from_db()
            serializer = BookSerializer(found_book)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"datail":"quantity field is missing"}, status=status.HTTP_400_BAD_REQUEST)
    

class CopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...