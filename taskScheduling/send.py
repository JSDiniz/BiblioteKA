
from books.models import Book, Follow
from copies.models import Copy
from users.models import User
from django.shortcuts import get_object_or_404

from .messageEmail import copyInventory
from .connectEmailSend import connectEmailSend
import time


def sendEmailFollowBook(user, book):
    body = copyInventory(user, book)
    return connectEmailSend(user, body)


def  sendEmailCopyBook(book_id):
    follow = Follow.objects.filter(book_id=book_id)

    for user_book in follow:
        book = get_object_or_404(Book, pk=user_book.book.id)
        user = get_object_or_404(User, pk=user_book.user_id)

        body = copyInventory(user, book)
        connectEmailSend(user, body)

def sendEmailFollowBookUser(data, tempo):
    time.sleep(tempo)
    sendEmailFollowBook(data["user"], data["book"])


def sendEmailCopyBookUser(data, tempo):
    copy = Copy.objects.filter(book_id=data, is_avaliable=True)

    if copy.count() <= 1:
        time.sleep(tempo)
        sendEmailCopyBook(data)


def sendEmailBookLoan(book_copy, tempo):
    copy = Copy.objects.filter(id=book_copy).first()
    book = Copy.objects.filter(book_id=copy.book_id, is_avaliable=True)

    if book.count() <= 1:
        time.sleep(tempo)
        sendEmailCopyBook(copy.book_id)


def bookReturn(data, tempo):
    copy = Copy.objects.filter(book_id=data.book_id, is_avaliable=True)

    if copy.count() <= 1:
        time.sleep(tempo)
        sendEmailCopyBook(data.book_id)