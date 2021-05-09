from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'name@example.com'}),
            'username': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control'})
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['user', 'title', 'document', 'subject', 'doc_type']
