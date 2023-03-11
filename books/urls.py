from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<pk>/", views.BookDetailView.as_view()),
    path("books/follow/<str:pk>/", views.FollowView.as_view()),
]
