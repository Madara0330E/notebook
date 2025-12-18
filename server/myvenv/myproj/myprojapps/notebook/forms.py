from django import forms
from .models import Person, Contact, Relationship

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'patronymic', 'birth_date', 'gender', 'workplace', 'position', 'notes']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['phone', 'email', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ['related_person', 'relationship_type', 'note']
        widgets = {
            'related_person': forms.Select(attrs={'class': 'form-control'}),
            'relationship_type': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
