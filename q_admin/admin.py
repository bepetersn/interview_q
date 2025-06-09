from django.contrib import admin
from django.utils.timezone import localtime
from apps.core.models import QuestionLog


class QuestionLogAdmin(admin.ModelAdmin):
    list_display = ("question", "outcome", "formatted_date_attempted")

    @admin.display(description="Date Attempted")
    def formatted_date_attempted(self, obj):
        return localtime(obj.date_attempted).date()

    readonly_fields = ("formatted_date_attempted",)


# Commenting out QuestionAdmin temporarily to resolve migration issues
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'difficulty', 'is_active', 'created_at')
#     filter_horizontal = ('topic_tags',)

# admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionLog, QuestionLogAdmin)
