from rest_framework.routers import DefaultRouter

from borrowing.views import BorrowingViewSet

app_name = "borrowing"

router = DefaultRouter()
router.register(r"borrowings", BorrowingViewSet)

urlpatterns = router.urls
