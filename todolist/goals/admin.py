from django.contrib import admin

from todolist.goals.models import GoalCategory, GoalComment, Goal


# class GoalCategoryAdmin(admin.ModelAdmin):
#     list_display = ("title", "user", "created", "updated")
#     search_fields = ("title", "user__username")
#
#
# admin.site.register(GoalCategory, GoalCategoryAdmin)
@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "description")


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "created", "updated")
    search_fields = ("text",)
