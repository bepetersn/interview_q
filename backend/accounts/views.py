from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from backend.core.serializers import RegisterSerializer, LoginSerializer
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
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
        user_data = UserSerializer(user).data
        # Store user info in session for whoami
        request.session["whoami"] = user_data
        return Response(user_data)


class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Remove whoami info from session on logout
        if "whoami" in request.session:
            del request.session["whoami"]
        logout(request)
        return Response({"detail": "Logged out"})


class IdentityView(APIView):
    # No IsAuthenticated permission, allow all

    def get(self, request, *args, **kwargs):
        # NOTE: Per-session caching of user info means that if the user updates their profile in another tab or device,
        # this session may show stale info until the cache is refreshed (e.g., after logout/login or manual update).
        # This is a common tradeoff for performance and is usually acceptable for most applications.
        if not request.user.is_authenticated:
            return Response(
                {"authenticated": False, "user": None}, status=status.HTTP_200_OK
            )

        # Check if user info is already in session
        data = request.session.get("whoami")
        if data:
            return Response(
                {"authenticated": True, "user": data}, status=status.HTTP_200_OK
            )

        user = request.user
        data = request.session["whoami"] = UserSerializer(user).data
        return Response(
            {"authenticated": True, "user": data}, status=status.HTTP_200_OK
        )
