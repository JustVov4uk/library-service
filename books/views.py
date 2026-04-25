from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny

from books.models import Book
from books.serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == "GET":
           return [AllowAny()]
        return [IsAdminUser()]
