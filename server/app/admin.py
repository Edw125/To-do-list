from django.contrib import admin

from app.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "status", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    empty_value_display = "-empty-"


admin.site.register(Task, TaskAdmin)
