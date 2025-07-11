from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from resumes.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('resumes/', include('resumes.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
