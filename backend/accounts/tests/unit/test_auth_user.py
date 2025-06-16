import pytest
from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch, reverse

# flake8: noqa

User = get_user_model()


@pytest.mark.parametrize("_", [None], ids=["create-user-succeeds"])
@pytest.mark.django_db
def test_create_user(_):
    user = User.objects.create_user(username="testuser", password="testpass123")
    assert user.username == "testuser"
    assert user.check_password("testpass123")
    assert user.is_active


@pytest.mark.parametrize("_", [None], ids=["create-superuser-succeeds"])
@pytest.mark.django_db
def test_create_superuser(_):
    user = User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpass123"
    )
    assert user.is_superuser
    assert user.is_staff


@pytest.mark.parametrize("_", [None], ids=["user-authentication-succeeds"])
@pytest.mark.django_db
def test_user_authentication(_, client):
    get_user_model().objects.create_user(username="authuser", password="authpass123")
    login = client.login(username="authuser", password="authpass123")
    assert login


@pytest.mark.parametrize("_", [None], ids=["user-login-view-succeeds"])
@pytest.mark.django_db
def test_user_login_view(_, client):
    get_user_model().objects.create_user(username="loginuser", password="loginpass123")
    try:
        url = reverse("accounts-login")
    except NoReverseMatch:
        url = "/api/accounts/login/"
    response = client.post(
        url,
        {"username": "loginuser", "password": "loginpass123"},
        content_type="application/json",
    )
    assert response.status_code in (200, 201, 204)


@pytest.mark.parametrize("_", [None], ids=["user-logout-view-succeeds"])
@pytest.mark.django_db
def test_user_logout_view(_, client):
    get_user_model().objects.create_user(
        username="logoutuser", password="logoutpass123"
    )
    client.login(username="logoutuser", password="logoutpass123")
    try:
        url = reverse("accounts-logout")
    except NoReverseMatch:
        url = "/api/accounts/logout/"
    response = client.post(url)
    assert response.status_code in (200, 201, 204)
