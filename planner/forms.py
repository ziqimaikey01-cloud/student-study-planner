from django import forms
from .models import Course, Assignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'due_date', 'completed']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['course'].queryset = Course.objects.filter(owner=user)