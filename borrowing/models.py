from django.contrib.auth import get_user_model
from django.db import models
from books.models import Book

User = get_user_model()


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book}, {self.borrow_date} - {self.expected_return_date}"
