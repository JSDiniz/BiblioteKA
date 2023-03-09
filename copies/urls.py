from django.urls import path
from . import views


urlpatterns = [
    path("books/<str:pk>/copy/", views.CopyView.as_view()),
]
