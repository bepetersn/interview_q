from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from backend.core.serializers import RegisterSerializer, LoginSerializer
import logging

# flake8: noqa

logger = logging.getLogger(__name__)


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            logger.warning(f"Register failed: invalid data: {serializer.errors}")
            return Response(
                {"detail": "Invalid data", "errors": serializer.errors}, status=400
            )
        self.perform_create(serializer)
        logger.info(
            f"User {serializer.validated_data.get('username', '<unknown>')} registered successfully."
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            logger.warning(f"Login failed: invalid data: {serializer.errors}")
            return Response(
                {"detail": "Invalid data", "errors": serializer.errors}, status=400
            )
        user = serializer.validated_data.get("user")
        if not user:
            logger.warning(
                f"Login failed: no user returned for data: {serializer.validated_data}"
            )
            return Response({"detail": "Invalid credentials"}, status=400)
        login(request, user)
        logger.info(f"User {user.username} logged in successfully.")
        return Response({"detail": "Logged in"})


class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out"})
