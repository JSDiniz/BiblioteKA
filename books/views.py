from rest_framework import generics
import ipdb
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permission import IsAdminOrOwner, IsEmployeeOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import Request, Response, status
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from emailsSend.send import sendEmailFollowBook

class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrOwner]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FollowView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def list(self, request, book_id):

        follow = get_list_or_404(Follow, book_id=book_id)
        serializer = FollowSerializer(follow, many=True)
        
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        following = Book.objects.filter(id=self.kwargs['book_id'], book_followers=self.request.user.id)

        if following:
            return Response(
                {"message": "You were already following this book"}, status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        primary_key = self.kwargs['book_id']
        book = get_object_or_404(Book, pk=primary_key)

        sendEmailFollowBook(user=self.request.user, book=book)
        
        return serializer.save(user=self.request.user, book=book)


class FollowDetailView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    lookup_url_kwarg = "book_id"

    def destroy(self, request: Request, *args, **kwargs):
        # ipdb.set_trace()
        get_book = get_object_or_404(Book, pk=kwargs['book_id'])
        following = Follow.objects.filter(book= get_book, user=self.request.user).first()

        if following:
            self.perform_destroy(following)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "The user does not follow this book."}, status.HTTP_404_NOT_FOUND)