from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """טופס הרשמה מותאם"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # הוספת מחלקות CSS לשדות
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label


class CustomAuthenticationForm(AuthenticationForm):
    """טופס התחברות מותאם"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # הוספת מחלקות CSS לשדות
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label


class UserProfileForm(forms.ModelForm):
    """טופס עדכון פרופיל משתמש"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_picture', 'bio')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # הוספת מחלקות CSS לשדות
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control' 