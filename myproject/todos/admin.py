from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Task, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Fieldsets for better organization
    fieldsets = [
        (None, {
            'fields': ['name']
        }),
    ]
    
    # Changelist view configuration
    list_display = ('name', 'get_task_count')
    search_fields = ('name',)
    
    def get_task_count(self, obj):
        return obj.task_set.count()
    get_task_count.short_description = 'Number of Tasks'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Fieldsets for better organization and readability
    fieldsets = [
        (_('Basic Information'), {
            'fields': ['title', 'description']
        }),
        (_('Task Status'), {
            'fields': ['status', 'due_date']
        }),
        (_('Additional Details'), {
            'fields': ['tags'],
            'classes': ['collapse']
        }),
        (_('System Information'), {
            'fields': ['timestamp'],
            'classes': ['collapse']
        }),
    ]
    
    # Changelist view configuration
    list_display = (
        'title', 
        'status', 
        'timestamp', 
        'due_date', 
        'display_tags'
    )
    list_filter = (
        'status', 
        'timestamp', 
        'due_date', 
        'tags'
    )
    search_fields = ('title', 'description')
    
    # Read-only fields to prevent editing
    readonly_fields = ('timestamp',)
    
    # Many-to-many field display
    filter_horizontal = ('tags',)
    
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'
    
    # Custom change form
    def get_readonly_fields(self, request, obj=None):
        # Ensure timestamp is always read-only
        return self.readonly_fields + ('timestamp',)
    
    # Optional: Custom list display for better readability
    def get_list_display(self, request):
        return self.list_display
    
    # Optional: Custom list filter
    def get_list_filter(self, request):
        return self.list_filter
