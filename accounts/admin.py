from django.contrib import admin
from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'blood_group', 'profile_image')
    search_fields = ('user__username', 'full_name', 'blood_group')
    list_filter = ('blood_group',)
    readonly_fields = ('user',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
