from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<pk>/", views.BookDetailView.as_view()),
    path("books/follow/<str:book_id>/", views.FollowView.as_view()),
    path("books/follow/<str:book_id>/user/", views.FollowDetailView.as_view()),
]
