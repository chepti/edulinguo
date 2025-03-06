from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import User


@receiver(post_save, sender=User)
def check_streak(sender, instance, created, **kwargs):
    """
    בודק ומעדכן את רצף הלמידה של המשתמש
    """
    if not created and instance.last_activity:
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # אם המשתמש היה פעיל אתמול, נשמור על הרצף
        if instance.last_activity == yesterday:
            instance.increase_streak()
        # אם המשתמש לא היה פעיל אתמול אבל היה פעיל היום, נאפס את הרצף
        elif instance.last_activity < yesterday and instance.last_activity != today:
            instance.reset_streak()
            instance.increase_streak()  # מתחילים רצף חדש 