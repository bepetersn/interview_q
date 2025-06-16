from django.urls import path

from .views import IdentityView, LoginViewSet, LogoutViewSet, RegisterViewSet

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
    path(
        "accounts/identity/",
        IdentityView.as_view(),
        name="accounts-identity",
    ),
]
