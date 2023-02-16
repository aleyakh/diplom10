from django.contrib.auth.models import Group

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from todolist.core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Особенные даты', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(Group)
