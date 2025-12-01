from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    """Form for creating and editing TODOs."""
    
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'is_resolved']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter TODO title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Description (optional)'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
        }

