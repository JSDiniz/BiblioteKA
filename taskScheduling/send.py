
from books.models import Book, Follow
from users.models import User
from django.shortcuts import get_object_or_404

from .messageEmail import copyInventory
from .connectEmailSend import connectEmailSend
import time


def sendEmailFollowBook(user, book):
    body = copyInventory(user, book)
    return connectEmailSend(user, body)


def  sendEmailCopyBook(data):
    follow = Follow.objects.filter(book_id=data["id"])

    for user_book in follow:
        book = get_object_or_404(Book, pk=user_book.book.id)
        user = get_object_or_404(User, pk=user_book.user_id)

        body = copyInventory(user, book)
        connectEmailSend(user, body)

def sendEmailFollowBookUser(data, tempo):
    time.sleep(tempo)
    sendEmailFollowBook(data["user"], data["book"])


def sendEmailCopyBookUser(data, tempo):
    time.sleep(tempo)
    sendEmailCopyBook(data)
