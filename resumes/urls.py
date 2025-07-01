from django.urls import path
from resumes.views import (
    ResumeListView, ResumeCreateView, ResumeUpdateView,
    ResumeDetailsView, ResumePDFView
)

urlpatterns = [
    path('list/', ResumeListView.as_view(), name='resume_list'),
    path('create/', ResumeCreateView.as_view(), name='create_resume'),
    path('update/<int:pk>/', ResumeUpdateView.as_view(), name='update_resume'),
    path(
        'details/<int:pk>/',
        ResumeDetailsView.as_view(),
        name='resume_details'
    ),
    path('resume/<int:pk>/pdf/', ResumePDFView.as_view(), name='resume_pdf'),
]
