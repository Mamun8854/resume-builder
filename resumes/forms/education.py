from django.forms import inlineformset_factory
from resumes.models import Education, Resume

EducationFormSet = inlineformset_factory(
    Resume, Education,
    fields=['institution', 'degree', 'start_year', 'end_year'],
    extra=1,
    can_delete=True
)
