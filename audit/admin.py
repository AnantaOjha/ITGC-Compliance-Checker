from django.contrib import admin
from .models import System, UserProfile, AccessLog, ChangeLog

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'last_modified_by']
    search_fields = ['name']
    
    def save_model(self, request, obj, form, change):
        obj.last_modified_by = request.user  # Track who made the change
        super().save_model(request, obj, form, change)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department']
    search_fields = ['user__username', 'role']

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'timestamp', 'ip_address']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['user__username']

@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'change_type', 'model_name', 'timestamp']
    list_filter = ['change_type', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name']