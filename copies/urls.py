from django.urls import path

from . import views

urlpatterns = [
    path("books/<str:pk>/copy/", views.CopyView.as_view()),
    path("copy/", views.ListCopiesView.as_view()),
    path("users/<str:user_id>/copy/<str:copy_id>/loan/", views.LoanView.as_view()),
    path("books/<str:pk>/follow/", views.LoanView.as_view()),
    path("loans/", views.ListLoanView.as_view()),
    path("loans/<str:pk>/", views.LoanDetailView.as_view()),
    path("users/<str:user_id>/loan/", views.LoanDetailView.as_view()),
]