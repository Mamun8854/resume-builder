import logging
# django imports for resumes class-based views
from django.views.generic import (
    TemplateView, CreateView, UpdateView, ListView, View
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
# local imports for models and forms
from resumes.models import Resume
from resumes.forms.resume import (
    ResumeForm, EducationFormSet,
    ExperienceFormSet, SkillFormSet
)

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

    def get_formset_kwargs(self, prefix):
        """Helper method to get consistent formset kwargs"""
        return {
            'instance': self.object,
            'prefix': prefix,
            'data': self.request.POST if self.request.method == 'POST' else None,  # noqa
            'files': self.request.FILES if self.request.method == 'POST' else None  # noqa
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['education_formset'] = EducationFormSet(
                **self.get_formset_kwargs('education'))
            context['experience_formset'] = ExperienceFormSet(
                **self.get_formset_kwargs('experience'))
            context['skill_formset'] = SkillFormSet(
                **self.get_formset_kwargs('skill'))
        else:
            context['education_formset'] = EducationFormSet(
                **self.get_formset_kwargs('education'))
            context['experience_formset'] = ExperienceFormSet(
                **self.get_formset_kwargs('experience'))
            context['skill_formset'] = SkillFormSet(
                **self.get_formset_kwargs('skill'))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        education_formset = context['education_formset']
        experience_formset = context['experience_formset']
        skill_formset = context['skill_formset']

        if all([
            form.is_valid(),
            education_formset.is_valid(),
            experience_formset.is_valid(),
            skill_formset.is_valid()
        ]):
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            # Save formsets
            education_formset.instance = self.object
            education_formset.save()

            experience_formset.instance = self.object
            experience_formset.save()

            skill_formset.instance = self.object
            skill_formset.save()

            messages.success(self.request, "Resume created successfully!")
            return redirect(self.success_url)
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


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
        context['education'] = resume.education_set.all()
        context['skills'] = resume.skills.all()
        return context


class ResumePDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk, user=request.user)
        template = get_template('resumes/details_pdf.html')
        html_string = template.render({
            'resume': resume,
            'experience': resume.experience.all(),
            'education': resume.education_set.all(),
            'skills': resume.skills.all()
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{resume.full_name}.pdf"'

        HTML(
            string=html_string,
            base_url=request.build_absolute_uri()
        ).write_pdf(response)
        return response
