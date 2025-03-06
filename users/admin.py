from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAchievement


class CustomUserAdmin(UserAdmin):
    """מנהל מותאם למודל המשתמש"""
    list_display = ('username', 'email', 'points', 'streak', 'is_premium', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('מידע נוסף', {'fields': ('profile_picture', 'bio', 'points', 'streak', 'last_activity', 'is_premium')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAchievement) 