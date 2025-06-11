from django.urls import path
from .views import RegisterViewSet, LoginViewSet, LogoutViewSet

urlpatterns = [
    path(
        "accounts/register/",
        RegisterViewSet.as_view({"post": "create"}),
        name="accounts-register",
    ),
    path(
        "accounts/login/",
        LoginViewSet.as_view({"post": "create"}),
        name="accounts-login",
    ),
    path(
        "accounts/logout/",
        LogoutViewSet.as_view({"post": "create"}),
        name="accounts-logout",
    ),
]
