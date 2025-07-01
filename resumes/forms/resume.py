from django import forms
from django.forms import inlineformset_factory
from resumes.models import Resume, Education, Experience, Skill


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name',
            'email',
            'phone',
            'address',
            'summary',
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'})
        }


# Education Formset
EducationFormSet = inlineformset_factory(
    Resume, Education,
    fields=[
        'institution', 'degree', 'field_of_study',
        'start_year', 'end_year', 'description'
    ],
    extra=1,
    can_delete=True,
    widgets={
        'start_year': forms.NumberInput(attrs={'class': 'form-control'}),
        'end_year': forms.NumberInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'rows': 3}),
    }
)

# Experience Formset
ExperienceFormSet = inlineformset_factory(
    Resume, Experience,
    fields=['company', 'position', 'start_date', 'end_date', 'description'],
    extra=1,
    can_delete=True,
    widgets={
        'start_date': forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        'end_date': forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        'description': forms.Textarea(attrs={'rows': 3}),
    }
)

# Skill Formset
SkillFormSet = inlineformset_factory(
    Resume, Skill,
    fields=['name', 'proficiency'],
    extra=1,
    can_delete=True,
)
