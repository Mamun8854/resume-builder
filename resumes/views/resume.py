import logging
# django imports for resumes class-based views
from django.views.generic import (
    TemplateView, CreateView, UpdateView, ListView, View
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
# local imports for models and forms
from resumes.models import Resume
from resumes.forms.resume import ResumeForm
from resumes.forms.education import EducationFormSet
from resumes.forms.experience import ExperienceFormSet, SkillFormSet

# Set up logging
logger = logging.getLogger(__name__)


class DashboardView(TemplateView):
    template_name = 'resumes/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResumeListView(LoginRequiredMixin, ListView):
    """
    View to list all resumes for the logged-in user.
    """
    template_name = 'resumes/list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        logger.info(
            f"User {self.request.user.username} accessed their resume list.")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Resume.objects.filter(user=self.request.user)
        logger.info(
            f"User {self.request.user.username} accessed their resume list.")
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_create.html'
    success_url = reverse_lazy('resume_list')

    def get(self, request, *args, **kwargs):
        form = ResumeForm()
        education_formset = EducationFormSet()
        experience_formset = ExperienceFormSet()
        skill_formset = SkillFormSet()
        return render(request, self.template_name, {
            'form': form,
            'education_formset': education_formset,
            'experience_formset': experience_formset,
            'skill_formset': skill_formset
        })

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        education_formset = EducationFormSet(request.POST)
        experience_formset = ExperienceFormSet(request.POST)
        skill_formset = SkillFormSet(request.POST)

        if form.is_valid() and education_formset.is_valid() and experience_formset.is_valid() and skill_formset.is_valid():  # noqa
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            # Bind the resume instance to related forms
            education_formset.instance = resume
            experience_formset.instance = resume
            skill_formset.instance = resume

            education_formset.save()
            experience_formset.save()
            skill_formset.save()

            messages.success(
                request, "Resume and related information saved successfully.")
            return redirect(self.success_url)
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {
                'form': form,
                'education_formset': education_formset,
                'experience_formset': experience_formset,
                'skill_formset': skill_formset
            })


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update an existing resume.
    """
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_form.html'
    success_url = reverse_lazy('resume_list')

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def form_valid(self, form):
        logger.info(f"User {self.request.user.username} updated a resume.")
        messages.success(self.request, "Resume updated successfully.")
        form.instance.user = self.request.user  # Ensure the user is set
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"User {self.request.user.username} submitted an invalid resume update form.")  # noqa
        messages.error(self.request, "There was an error updating your resume. Please correct the errors below.")  # noqa
        return super().form_invalid(form)


class ResumeDetailsView(LoginRequiredMixin, TemplateView):
    """
    View to display the details of a specific resume for the logged-in user.
    """
    template_name = 'resumes/details.html'

    def get_object(self):
        return Resume.objects.get(id=self.kwargs['pk'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = self.get_object()
        context['resume'] = resume
        context['experience'] = resume.experience.all()
        context['education'] = resume.education.all()
        context['skills'] = resume.skills.all()
        return context


class ResumePDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk, user=request.user)
        template = get_template('resumes/details_pdf.html')
        html_string = template.render({
            'resume': resume,
            'experience': resume.experience.all(),
            'education': resume.education.all(),
            'skills': resume.skills.all()
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{resume.full_name}.pdf"'

        HTML(
            string=html_string,
            base_url=request.build_absolute_uri()
        ).write_pdf(response)
        return response
