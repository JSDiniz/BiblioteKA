from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import  Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from users.models import User
from users.permission import IsAdminOrOwner
from books.serializers import BookSerializer

from .models import Copy, Loan
from .permissions import IsAdminOrLoanOwner
from .serializers import CopySerializer, LoanSerializer
from taskScheduling.send import sendEmailCopyBookUser
import threading

class CopyView(generics.CreateAPIView):
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


            email = threading.Thread(target=sendEmailCopyBookUser, args=(serializer.data, 5))
            email.start()

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


class CopyDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    lookup_url_kwarg = "copy_id"


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

        return Loan.objects.filter(borrower=self.request.user)



class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrLoanOwner]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_update(self, serializer):
        serializer.save()
        # ipdb.set_trace()
        expires = LoanSerializer(serializer.instance)
        loan = serializer.instance
        copy = loan.book_copy
        user = loan.borrower
        
        if not copy.is_avaliable and loan.refund_at > expires.data["expires_at"]:
            print('maior')
            user.is_blocked = True
            user.save()

        copy.is_available = True
        copy.save()
        copy.borrowers.remove(user)

