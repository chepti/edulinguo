from django.contrib import admin
from .models import LearningGoal, DailyChallenge, UserDailyChallenge, Notification


@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'target_date', 'completed')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    filter_horizontal = ('related_courses',)


@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'points', 'learning_atom')
    list_filter = ('date',)
    search_fields = ('title', 'description')


@admin.register(UserDailyChallenge)
class UserDailyChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'completed', 'completed_at')
    list_filter = ('completed', 'challenge__date')
    search_fields = ('user__username', 'challenge__title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'created_at', 'read')
    list_filter = ('notification_type', 'read', 'created_at')
    search_fields = ('title', 'message', 'user__username') 