from rest_framework import viewsets

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingCreateSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        else:
            return BorrowingListSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
