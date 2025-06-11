from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.question_log import (
    QuestionLogListCreateView,
    QuestionLogRetrieveUpdateDestroyView,
    QuestionLogViewSet,
)
from .views.question import QuestionViewSet, QuestionListCreateView
from .views.tag import TagListCreateView, TagRetrieveDestroyView
from .views.auth import RegisterViewSet, LoginViewSet


router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"questionlogs", QuestionLogViewSet, basename="questionlog")

urlpatterns = [
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path(
        "questionlogs/",
        QuestionLogListCreateView.as_view(),
        name="questionlog-list-create",
    ),
    path(
        "questionlogs/<int:pk>/",
        QuestionLogRetrieveUpdateDestroyView.as_view(),
        name="questionlog-detail",
    ),
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagRetrieveDestroyView.as_view(), name="tag-detail"),
    path(
        "auth/register/",
        RegisterViewSet.as_view({"post": "create"}),
        name="auth-register",
    ),
    path(
        "auth/login/",
        LoginViewSet.as_view({"post": "create"}),
        name="auth-login",
    ),
]

urlpatterns += router.urls
