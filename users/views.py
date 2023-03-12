from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .permission import IsAdminOrOwner
from .serializers import UserSerializer


class UserView(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    serializer_class = [IsAuthenticated, IsAdminOrOwner]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = [IsAuthenticated, IsAdminOrOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"
