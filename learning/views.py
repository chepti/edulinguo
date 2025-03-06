from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from courses.models import Course, Category, UserCourse, UserProgress
from .models import LearningGoal, DailyChallenge, UserDailyChallenge, Notification
from .forms import LearningGoalForm


def home(request):
    """דף הבית של האתר"""
    # קורסים פופולריים
    popular_courses = Course.objects.filter(is_published=True).annotate(
        student_count=Count('enrolled_users')
    ).order_by('-student_count')[:6]
    
    # קטגוריות
    categories = Category.objects.all()
    
    # אתגר יומי
    today = timezone.now().date()
    daily_challenge = DailyChallenge.objects.filter(date=today).first()
    
    # בדיקה אם המשתמש השלים את האתגר היומי
    challenge_completed = False
    if request.user.is_authenticated and daily_challenge:
        challenge_completed = UserDailyChallenge.objects.filter(
            user=request.user, 
            challenge=daily_challenge,
            completed=True
        ).exists()
    
    context = {
        'popular_courses': popular_courses,
        'categories': categories,
        'daily_challenge': daily_challenge,
        'challenge_completed': challenge_completed,
    }
    
    return render(request, 'learning/home.html', context)


def about(request):
    """דף אודות"""
    return render(request, 'learning/about.html')


@login_required
def set_learning_goal(request):
    """הגדרת מטרת למידה חדשה"""
    if request.method == 'POST':
        form = LearningGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            
            # שמירת הקורסים הקשורים
            form.save_m2m()
            
            messages.success(request, "מטרת הלמידה נוצרה בהצלחה!")
            return redirect('dashboard')
    else:
        form = LearningGoalForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'learning/set_learning_goal.html', context)


@login_required
def learning_goals(request):
    """תצוגת מטרות הלמידה של המשתמש"""
    goals = LearningGoal.objects.filter(user=request.user)
    
    context = {
        'goals': goals,
    }
    
    return render(request, 'learning/learning_goals.html', context)


@login_required
def complete_daily_challenge(request, challenge_id):
    """השלמת אתגר יומי"""
    challenge = get_object_or_404(DailyChallenge, id=challenge_id)
    
    # בדיקה אם האתגר כבר הושלם
    user_challenge, created = UserDailyChallenge.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )
    
    if not user_challenge.completed:
        user_challenge.completed = True
        user_challenge.completed_at = timezone.now()
        user_challenge.save()
        
        # הוספת נקודות למשתמש
        request.user.add_points(challenge.points)
        
        messages.success(request, f"כל הכבוד! השלמת את האתגר היומי וקיבלת {challenge.points} נקודות")
    else:
        messages.info(request, "כבר השלמת את האתגר היומי")
    
    return redirect('home')


@login_required
def notifications(request):
    """תצוגת ההתראות של המשתמש"""
    notifications = Notification.objects.filter(user=request.user)
    
    # סימון כל ההתראות כנקראו
    unread_notifications = notifications.filter(read=False)
    unread_notifications.update(read=True)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'learning/notifications.html', context)


@login_required
def leaderboard(request):
    """לוח המובילים"""
    top_users = User.objects.order_by('-points')[:20]
    
    # מיקום המשתמש הנוכחי
    user_rank = User.objects.filter(points__gt=request.user.points).count() + 1
    
    context = {
        'top_users': top_users,
        'user_rank': user_rank,
    }
    
    return render(request, 'learning/leaderboard.html', context) 