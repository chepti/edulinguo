from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Category, Course, Unit, LearningAtom, UserCourse, UserProgress


def course_list(request):
    """תצוגת רשימת הקורסים"""
    categories = Category.objects.all()
    courses = Course.objects.filter(is_published=True)
    
    # סינון לפי קטגוריה אם צוינה
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        courses = courses.filter(category=category)
    
    # סינון לפי רמת קושי אם צוינה
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    context = {
        'categories': categories,
        'courses': courses,
    }
    
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    """תצוגת פרטי קורס"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    units = course.units.all()
    
    # בדיקה אם המשתמש רשום לקורס
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = UserCourse.objects.filter(user=request.user, course=course).exists()
    
    context = {
        'course': course,
        'units': units,
        'is_enrolled': is_enrolled,
    }
    
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    """הרשמה לקורס"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    # בדיקה אם המשתמש כבר רשום לקורס
    if UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "אתה כבר רשום לקורס זה")
    else:
        UserCourse.objects.create(user=request.user, course=course)
        messages.success(request, f"נרשמת בהצלחה לקורס {course.title}")
    
    return redirect('course_detail', slug=slug)


@login_required
def unit_detail(request, course_slug, unit_order):
    """תצוגת פרטי יחידת לימוד"""
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    unit = get_object_or_404(Unit, course=course, order=unit_order)
    atoms = unit.atoms.all()
    
    # בדיקה אם המשתמש רשום לקורס
    if not UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, "עליך להירשם לקורס כדי לצפות ביחידות הלימוד")
        return redirect('course_detail', slug=course_slug)
    
    # מידע על התקדמות המשתמש
    progress = {}
    for atom in atoms:
        progress[atom.id] = UserProgress.objects.filter(user=request.user, atom=atom).first()
    
    context = {
        'course': course,
        'unit': unit,
        'atoms': atoms,
        'progress': progress,
    }
    
    return render(request, 'courses/unit_detail.html', context)


@login_required
def atom_detail(request, course_slug, unit_order, atom_order):
    """תצוגת אטום למידה"""
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    unit = get_object_or_404(Unit, course=course, order=unit_order)
    atom = get_object_or_404(LearningAtom, unit=unit, order=atom_order)
    
    # בדיקה אם המשתמש רשום לקורס
    if not UserCourse.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, "עליך להירשם לקורס כדי לצפות בתוכן")
        return redirect('course_detail', slug=course_slug)
    
    # מידע על התקדמות המשתמש
    progress, created = UserProgress.objects.get_or_create(user=request.user, atom=atom)
    
    # עדכון תאריך הפעילות האחרון של המשתמש
    request.user.last_activity = timezone.now().date()
    request.user.save()
    
    context = {
        'course': course,
        'unit': unit,
        'atom': atom,
        'progress': progress,
    }
    
    return render(request, 'courses/atom_detail.html', context)


@login_required
def complete_atom(request, atom_id):
    """סימון אטום למידה כהושלם"""
    atom = get_object_or_404(LearningAtom, id=atom_id)
    
    # בדיקה אם המשתמש רשום לקורס
    if not UserCourse.objects.filter(user=request.user, course=atom.unit.course).exists():
        messages.warning(request, "עליך להירשם לקורס כדי להשלים פעילויות")
        return redirect('course_detail', slug=atom.unit.course.slug)
    
    # עדכון התקדמות המשתמש
    progress, created = UserProgress.objects.get_or_create(user=request.user, atom=atom)
    
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # הוספת נקודות למשתמש
        request.user.add_points(atom.points)
        messages.success(request, f"כל הכבוד! קיבלת {atom.points} נקודות")
    
    # בדיקה אם היחידה הושלמה
    unit_atoms = atom.unit.atoms.all()
    completed_atoms = UserProgress.objects.filter(
        user=request.user, 
        atom__unit=atom.unit, 
        completed=True
    ).count()
    
    if completed_atoms == unit_atoms.count():
        messages.success(request, f"השלמת את היחידה {atom.unit.title}!")
    
    # בדיקה אם הקורס הושלם
    course_atoms_count = LearningAtom.objects.filter(unit__course=atom.unit.course).count()
    completed_course_atoms = UserProgress.objects.filter(
        user=request.user, 
        atom__unit__course=atom.unit.course, 
        completed=True
    ).count()
    
    if completed_course_atoms == course_atoms_count:
        user_course = UserCourse.objects.get(user=request.user, course=atom.unit.course)
        user_course.completed = True
        user_course.save()
        messages.success(request, f"כל הכבוד! השלמת את הקורס {atom.unit.course.title}!")
    
    # מעבר לאטום הבא אם קיים
    next_atom = LearningAtom.objects.filter(
        unit=atom.unit, 
        order__gt=atom.order
    ).order_by('order').first()
    
    if next_atom:
        return redirect('atom_detail', 
                       course_slug=atom.unit.course.slug, 
                       unit_order=atom.unit.order, 
                       atom_order=next_atom.order)
    
    # אם אין אטום נוסף ביחידה, מעבר ליחידה הבאה אם קיימת
    next_unit = Unit.objects.filter(
        course=atom.unit.course, 
        order__gt=atom.unit.order
    ).order_by('order').first()
    
    if next_unit:
        first_atom = next_unit.atoms.order_by('order').first()
        if first_atom:
            return redirect('atom_detail', 
                           course_slug=atom.unit.course.slug, 
                           unit_order=next_unit.order, 
                           atom_order=first_atom.order)
    
    # אם אין יחידה נוספת, חזרה לדף הקורס
    return redirect('course_detail', slug=atom.unit.course.slug) 