from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    מודל משתמש מותאם המרחיב את המודל הבסיסי של Django
    """
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    last_activity = models.DateField(null=True, blank=True)
    
    # שדות נוספים שיכולים להיות שימושיים
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def increase_streak(self):
        """מגדיל את רצף הלמידה של המשתמש"""
        self.streak += 1
        self.save()
    
    def reset_streak(self):
        """מאפס את רצף הלמידה של המשתמש"""
        self.streak = 0
        self.save()
    
    def add_points(self, amount):
        """מוסיף נקודות למשתמש"""
        self.points += amount
        self.save()


class UserAchievement(models.Model):
    """
    מודל המייצג הישגים שהמשתמש השיג
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievement_icons')
    date_earned = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}" 