import logging
# django imports for resumes class-based views
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# local imports for models and forms
from resumes.models import Resume
from resumes.forms.resume import ResumeForm

# Set up logging
logger = logging.getLogger(__name__)


class DashboardView(TemplateView):
    template_name = 'resumes/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResumeListView(TemplateView):
    """
    View to list all resumes for the logged-in user.
    """
    template_name = 'resumes/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['resumes'] = Resume.objects.filter(user=self.request.user)
        # logger.info(f"User {self.request.user.username} accessed their resume list.")
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new resume.
    """
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_create.html'
    success_url = reverse_lazy('resume_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "Resume created successfully.")
        logger.info(f"User {self.request.user.username} created a new resume.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"User {self.request.user.username} submitted an invalid resume form.")
        messages.error(self.request, "There was an error creating your resume. Please correct the errors below.")
        return super().form_invalid(form)


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
        logger.error(f"User {self.request.user.username} submitted an invalid resume update form.")
        messages.error(self.request, "There was an error updating your resume. Please correct the errors below.")
        return super().form_invalid(form)
