from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from users.permission import IsAdminOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    
    authentication_classes = [JWTAuthentication]
    serializer_class = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    serializer_class = [IsAdminOrOwner]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
