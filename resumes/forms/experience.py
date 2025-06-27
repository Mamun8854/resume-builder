from django import forms
from resumes.models import Experience, Skill

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        exclude = ['resume']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['resume']
