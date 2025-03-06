# Generated by Django 4.2.7 on 2025-03-06 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0001_initial'),
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdailychallenge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_challenges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='learninggoal',
            name='related_courses',
            field=models.ManyToManyField(blank=True, related_name='learning_goals', to='courses.course'),
        ),
        migrations.AddField(
            model_name='learninggoal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_goals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dailychallenge',
            name='learning_atom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.learningatom'),
        ),
        migrations.AlterUniqueTogether(
            name='userdailychallenge',
            unique_together={('user', 'challenge')},
        ),
    ]
