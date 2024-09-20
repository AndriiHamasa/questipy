from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import Project, TaskType, Position, Worker, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", )}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "is_completed", "priority", "project", "task_type")
    search_fields = ("name", )
    list_filter = ("is_completed", "task_type")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name", )


admin.site.register(TaskType)
admin.site.register(Position)
