from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrowing.models import Borrowing
from helpers.notifications import send_telegram_notifications


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )

    def validate(self, data):
        if data["book"].inventory == 0:
            raise serializers.ValidationError("Book is out of inventory")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(user=user, **validated_data)
        send_telegram_notifications(
            f"New borrowing: {borrowing.book.title},"
            f"User: {borrowing.user.email},"
            f"Due date: {borrowing.expected_return_date},"
        )
        return borrowing
