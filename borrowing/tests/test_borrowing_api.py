from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from books.models import Book
from borrowing.models import Borrowing


def borrowing_url():
    return reverse("borrowing:borrowing-list")

def borrowing_return_url(pk):
    return reverse("borrowing:borrowing-borrowing-return", args=[pk])


class BorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@email",
            password="PASSWORD",
        )
        self.other_user = get_user_model().objects.create(
            email="other_user@email",
            password="PASSWORD1",
        )
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=100.00
        )

    def test_create_borrowing(self):
        payload = {
            "borrow_date": "2026-04-10",
            "expected_return_date": "2026-05-10",
            "book": self.book.id,
        }
        result = self.client.post(borrowing_url(), payload)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 9)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_create_borrowing_with_inventory_0(self):
        self.book.inventory = 0
        self.book.save()
        payload = {
            "borrow_date": "2026-04-10",
            "expected_return_date": "2026-05-10",
            "book": self.book.id,
        }
        result = self.client.post(borrowing_url(), payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_see_only_own_borrowing(self):
        Borrowing.objects.create(
            borrow_date="2026-04-10",
            expected_return_date="2026-05-10",
            book=self.book,
            user=self.user,
        )
        Borrowing.objects.create(
            borrow_date="2026-04-10",
            expected_return_date="2026-05-10",
            book=self.book,
            user=self.other_user,
        )
        result = self.client.get(borrowing_url())
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result.data), 1)

    def test_return_inventory_success(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2026-04-10",
            expected_return_date="2026-05-10",
            book=self.book,
            user=self.user,
        )
        result = self.client.post(borrowing_return_url(borrowing.id))
        self.book.refresh_from_db()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book.inventory, 11)

    def test_return_inventory_failure(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2026-04-10",
            expected_return_date="2026-05-10",
            book=self.book,
            user=self.user,
        )
        result = self.client.post(borrowing_return_url(borrowing.id))
        result1 = self.client.post(borrowing_return_url(borrowing.id))
        self.book.refresh_from_db()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result1.status_code, status.HTTP_400_BAD_REQUEST)
