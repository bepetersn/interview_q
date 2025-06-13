from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.question_log import (
    QuestionLogListCreateView,
    QuestionLogRetrieveUpdateDestroyView,
)
from .views.question import QuestionViewSet
from .views.tag import TagListCreateView, TagRetrieveUpdateDestroyView


router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = [
    path(
        "questions/<int:question_id>/logs/",
        QuestionLogListCreateView.as_view(),
        name="questionlog-list-create",
    ),
    path(
        "questions/<int:question_id>/logs/<int:pk>/",
        QuestionLogRetrieveUpdateDestroyView.as_view(),
        name="questionlog-detail",
    ),
    path("tags/", TagListCreateView.as_view(), name="tag-list-create"),
    path("tags/<int:pk>/", TagRetrieveUpdateDestroyView.as_view(), name="tag-detail"),
]

urlpatterns += router.urls
