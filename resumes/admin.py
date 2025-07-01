from django.contrib import admin
from resumes.models import Resume, Experience, Skill, Education


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 1
    fields = ('company', 'position', 'start_date', 'end_date', 'description')
    show_change_link = True


class EducationInline(admin.StackedInline):
    model = Education
    extra = 1
    fields = ('institution', 'degree', 'start_year', 'end_year')
    show_change_link = True


class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1
    fields = ('name', 'proficiency')
    show_change_link = True


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    inlines = [ExperienceInline, EducationInline, SkillInline]
