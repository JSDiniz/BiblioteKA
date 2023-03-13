from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
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

    def get(self, request, pk):
        follow = get_list_or_404(Follow, user_id=pk)
        serializer = FollowSerializer(follow, many=True)
        
        return Response(serializer.data)

    def post(self, request: Request, pk: str):
        book = get_object_or_404(Book, pk=pk)

        following = Follow.objects.filter(book_id=book.id, user_id=self.request.user.id).first()

        if following:
            return Response(
                {"message": "You were already following this book"}, status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        follow_obj = serializer.save(book=book, user=self.request.user)

        serializer = FollowSerializer(follow_obj)

        sendEmailFollowBook(self.request.user, book)

        return Response(serializer.data, status.HTTP_201_CREATED)


class FollowDetailView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    
    lookup_url_kwarg = "pk"
