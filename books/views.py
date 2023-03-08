from .models import Book
from rest_framework import generics
from .serializers import BookSerializer
from users.permission import IsAdminOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


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
