from django.contrib import admin
from resumes.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
