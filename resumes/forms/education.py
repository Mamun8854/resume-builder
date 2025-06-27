from django import forms
from resumes.models import Education

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
        exclude = ['resume']
