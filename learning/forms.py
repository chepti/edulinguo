from django import forms
from .models import LearningGoal
from courses.models import Course


class LearningGoalForm(forms.ModelForm):
    """טופס ליצירת מטרת למידה חדשה"""
    
    class Meta:
        model = LearningGoal
        fields = ['title', 'description', 'target_date', 'related_courses']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'related_courses': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # הוספת מחלקות CSS לשדות
        for field_name in self.fields:
            if field_name != 'related_courses':
                self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        # הגבלת הקורסים לקורסים פעילים בלבד
        self.fields['related_courses'].queryset = Course.objects.filter(is_published=True) 