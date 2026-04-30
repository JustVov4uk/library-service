from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from borrowing.models import Borrowing
from borrowing.serializers import (BorrowingListSerializer,
                                   BorrowingCreateSerializer)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        else:
            return BorrowingListSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
        permission_classes=[IsAuthenticated],
    )
    def borrowing_return(self, request, pk=None):
        borrowing = Borrowing.objects.get(pk=pk)
        if borrowing.actual_return_date is not None:
            return Response({"error": "Already returned"}, status=400)
        borrowing.actual_return_date = timezone.now().date()
        borrowing.book.inventory += 1
        borrowing.save()
        borrowing.book.save()
        return Response(BorrowingListSerializer(borrowing).data)
