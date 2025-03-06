from django.db import models
from django.utils.text import slugify
from users.models import User


class Category(models.Model):
    """
    קטגוריה של חומרי לימוד (למשל: מתמטיקה, שפות, מדעים)
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category_icons', blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    """
    קורס מלא המכיל מספר יחידות לימוד
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='course_images', blank=True, null=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    # מידע נוסף
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'מתחילים'),
        ('intermediate', 'בינוני'),
        ('advanced', 'מתקדם'),
    ], default='beginner')
    estimated_duration = models.PositiveIntegerField(help_text="משך זמן משוער בדקות", null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Unit(models.Model):
    """
    יחידת לימוד בתוך קורס
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class LearningAtom(models.Model):
    """
    אטום למידה - יחידת הלימוד הקטנה ביותר
    """
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='atoms')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=[
        ('text', 'טקסט'),
        ('video', 'וידאו'),
        ('quiz', 'שאלון'),
        ('exercise', 'תרגיל'),
        ('flashcard', 'כרטיסיות'),
    ])
    content = models.TextField(help_text="תוכן או קישור לתוכן")
    explanation = models.TextField(blank=True, null=True, help_text="הסבר נוסף או רמזים")
    order = models.PositiveIntegerField(default=1)
    points = models.PositiveIntegerField(default=10, help_text="נקודות שהמשתמש מקבל על השלמת האטום")
    
    class Meta:
        ordering = ['order']
        unique_together = ['unit', 'order']
    
    def __str__(self):
        return f"{self.unit.title} - {self.title}"


class UserProgress(models.Model):
    """
    מעקב אחר התקדמות המשתמש בקורסים
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    atom = models.ForeignKey(LearningAtom, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0, help_text="ציון שהמשתמש קיבל (אם רלוונטי)")
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'atom']
    
    def __str__(self):
        return f"{self.user.username} - {self.atom.title}"


class UserCourse(models.Model):
    """
    קורסים שהמשתמש נרשם אליהם
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_users')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}" 