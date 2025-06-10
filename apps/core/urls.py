from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    QuestionLogListCreateView,
    QuestionLogRetrieveUpdateDestroyView,
    TagListCreateView,
    TagRetrieveUpdateDestroyView,
    QuestionViewSet,
    QuestionLogViewSet,
    QuestionListCreateView,
)

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
    path("tags/<int:pk>/", TagRetrieveUpdateDestroyView.as_view(), name="tag-detail"),
]

urlpatterns += router.urls
