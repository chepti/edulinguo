from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('goals/', views.learning_goals, name='learning_goals'),
    path('goals/new/', views.set_learning_goal, name='set_learning_goal'),
    path('challenge/<int:challenge_id>/complete/', views.complete_daily_challenge, name='complete_daily_challenge'),
    path('notifications/', views.notifications, name='notifications'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
] 