from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from ..serializers import RegisterSerializer, LoginSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data["user"])
        return Response({"detail": "Logged in"})
