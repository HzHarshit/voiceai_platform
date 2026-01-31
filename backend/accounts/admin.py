from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'tenant', 'is_active', 'date_joined')
    list_filter = ('tenant', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'tenant__name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Tenant Information', {'fields': ('tenant',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Tenant Information', {'fields': ('tenant',)}),
    )
