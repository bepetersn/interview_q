from django.apps import AppConfig
from django.contrib import admin

from backend.core.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# @admin.register(QuestionLog)
# class QuestionLogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'difficulty', 'date_attempted', 'needs_review')
#     list_filter = ('difficulty', 'needs_review', 'date_attempted')
#     search_fields = ('title', 'source', 'solution_approach')
#     filter_horizontal = ('tags',)


class QAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.q_admin"
