from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from users.permission import IsAdminOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer


class BookView(generics.ListCreateAPIView):
    ...
    # authentication_classes = [JWTAuthentication]
    # serializer_class = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # def perform_create(self, serializer):
    #     return serializer.save(user_id=self.request.user.id)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    serializer_class = [IsAdminOrOwner]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FollowView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))
        return serializer.save(book=book, user=self.request.user)
