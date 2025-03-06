from django.db import models
from users.models import User
from courses.models import Course, LearningAtom


class LearningGoal(models.Model):
    """
    מטרת למידה שהמשתמש הגדיר
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    # קורסים הקשורים למטרה זו
    related_courses = models.ManyToManyField(Course, blank=True, related_name='learning_goals')
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class DailyChallenge(models.Model):
    """
    אתגר יומי שמוצג למשתמשים
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.PositiveIntegerField(default=20)
    date = models.DateField()
    
    # אפשרי לקשר לאטום למידה ספציפי
    learning_atom = models.ForeignKey(LearningAtom, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} - {self.title}"


class UserDailyChallenge(models.Model):
    """
    מעקב אחר השלמת אתגרים יומיים על ידי משתמשים
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'challenge']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class Notification(models.Model):
    """
    התראות למשתמשים
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    # סוגי התראות
    NOTIFICATION_TYPES = [
        ('achievement', 'הישג חדש'),
        ('streak', 'רצף למידה'),
        ('reminder', 'תזכורת'),
        ('system', 'הודעת מערכת'),
    ]
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}" 