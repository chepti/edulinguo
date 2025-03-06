from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User, UserAchievement


def register(request):
    """תצוגת הרשמה למשתמש חדש"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "נרשמת בהצלחה!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """תצוגת פרופיל המשתמש"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "הפרופיל עודכן בהצלחה!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    achievements = request.user.achievements.all()
    
    context = {
        'form': form,
        'achievements': achievements,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def dashboard(request):
    """תצוגת לוח המחוונים של המשתמש"""
    # כאן נוכל להציג את הקורסים של המשתמש, ההתקדמות שלו, וכו'
    return render(request, 'users/dashboard.html') 