from django.urls import path
from resumes.views import ResumeListView, ResumeCreateView, ResumeUpdateView

urlpatterns = [
    path('list/', ResumeListView.as_view(), name='resume_list'),
    path('create/', ResumeCreateView.as_view(), name='create_resume'),
    path('update/<int:pk>/', ResumeUpdateView.as_view(), name='update_resume'),
]
