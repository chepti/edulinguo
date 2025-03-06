from django.contrib import admin
from .models import Category, Course, Unit, LearningAtom, UserProgress, UserCourse


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1


class LearningAtomInline(admin.TabularInline):
    model = LearningAtom
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty_level', 'is_published')
    list_filter = ('category', 'difficulty_level', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [UnitInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    inlines = [LearningAtomInline]


@admin.register(LearningAtom)
class LearningAtomAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'content_type', 'order', 'points')
    list_filter = ('content_type', 'unit__course')
    search_fields = ('title', 'content')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'atom', 'completed', 'score', 'completed_at')
    list_filter = ('completed', 'atom__unit__course')
    search_fields = ('user__username', 'atom__title')


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'completed')
    list_filter = ('completed', 'course')
    search_fields = ('user__username', 'course__title') 