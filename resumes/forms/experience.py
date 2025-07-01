from django.forms import inlineformset_factory
from resumes.models import Experience, Skill, Resume

ExperienceFormSet = inlineformset_factory(
    Resume, Experience,
    fields=['company', 'position', 'start_date', 'end_date', 'description'],
    extra=1,
    can_delete=True
)

SkillFormSet = inlineformset_factory(
    Resume, Skill,
    fields=['name', 'proficiency'],
    extra=1,
    can_delete=True
)
