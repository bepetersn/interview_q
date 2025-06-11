import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse, NoReverseMatch

# flake8: noqa

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="testuser", password="testpass123")
    assert user.username == "testuser"
    assert user.check_password("testpass123")
    assert user.is_active


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpass123"
    )
    assert user.is_superuser
    assert user.is_staff


@pytest.mark.django_db
def test_user_authentication(client):
    user = User.objects.create_user(username="authuser", password="authpass123")
    login = client.login(username="authuser", password="authpass123")
    assert login


@pytest.mark.django_db
def test_user_login_view(client):
    user = User.objects.create_user(username="loginuser", password="loginpass123")
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


@pytest.mark.django_db
def test_user_logout_view(client):
    user = User.objects.create_user(username="logoutuser", password="logoutpass123")
    client.login(username="logoutuser", password="logoutpass123")
    try:
        url = reverse("accounts-logout")
    except NoReverseMatch:
        url = "/api/accounts/logout/"
    response = client.post(url)
    assert response.status_code in (200, 201, 204)
