from django import forms
from .models import Course, Assignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'due_date', 'completed']
    