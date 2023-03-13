from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<pk>/", views.BookDetailView.as_view()),
    path("books/follow/<str:pk>/", views.FollowView.as_view()),
    path("books/follow/<str:pk>/user/", views.FollowDetailView.as_view()),
]
