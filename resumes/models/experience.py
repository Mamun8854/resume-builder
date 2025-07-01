from django.db import models
from resumes.models import Resume


class Experience(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE,
        related_name='experience'
    )
    company = models.CharField(max_length=200, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=10, null=True, blank=True)
    end_date = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.position} at {self.company} ({self.start_date} - {self.end_date})"  # noqa


class Skill(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.proficiency})"
