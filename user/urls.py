from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import UserRegisterView, ManageUserView

app_name = "user"

urlpatterns = [
    path("users/", UserRegisterView.as_view(), name="user_register"),
    path("users/me/", ManageUserView.as_view(), name="user_me"),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
