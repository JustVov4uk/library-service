from django.urls import path

from books.views import BookView, BookDetailView

app_name = "books"

urlpatterns = [
    path("books/", BookView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
]
