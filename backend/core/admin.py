from django.contrib import admin

from .models import Question, QuestionLog, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_active", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "is_active", "created_at", "user")
    readonly_fields = ("slug", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("difficulty", "is_active", "created_at", "user")


@admin.register(QuestionLog)
class QuestionLogAdmin(admin.ModelAdmin):
    list_display = ("question", "user", "date_attempted", "outcome", "time_spent_min")
    search_fields = ("question__title", "solution_approach", "self_notes")
    list_filter = ("outcome", "date_attempted", "user")
