
from django import forms
from .models import SavedLink


class SavedLinkForm(forms.ModelForm):
    class Meta:
        model = SavedLink
        fields = [
            'title',
            'url',
            'category',
            'note',
            'is_visited',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Django documentation',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why do you want to save this link?',
            }),
            'is_visited': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
