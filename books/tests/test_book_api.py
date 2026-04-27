from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Book


def book_url(pk=None):
    if pk:
        return reverse("books:book-detail", args=[pk])
    return reverse("books:book-list")


class AdminBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="TestPassword",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin)

    def test_admin_create_book(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 100.00
        }
        result = self.client.post(book_url(), payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)


class AuthenticatedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="user@gmail.com",
            password="Password",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book_authenticated_user_forbidden(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 100.00
        }
        result = self.client.post(book_url(), payload)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)


class UnauthorizedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list_unauthorized(self):
        result = self.client.get(book_url())
        self.assertEqual(result.status_code, status.HTTP_200_OK)


    def test_book_detail_unauthorized(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=100.00
        )
        result = self.client.get(book_url(pk=book.id))
        self.assertEqual(result.status_code, status.HTTP_200_OK)
