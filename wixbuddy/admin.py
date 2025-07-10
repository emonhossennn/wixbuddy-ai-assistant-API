from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import About, DashboardImage, Resource, Video, FAQ, Question
from adminsortable2.admin import SortableAdminMixin

admin.site.register(About)
admin.site.register(DashboardImage)

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    inlines = [VideoInline, FAQInline]
    list_display = ['name', 'created_at']



admin.site.register(Video)
admin.site.register(FAQ)

# Remove the default registration for Question
from django.contrib import admin
try:
    admin.site.unregister(Question)
except admin.sites.NotRegistered:
    pass

@admin.register(Question)
class QuestionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title', 'options', 'is_active', 'created_at')
    list_editable = ('title', 'options', 'is_active')  # Do NOT include 'order'
    ordering = ('order',)
    search_fields = ('title',)
    list_display_links = ()  # No clickable links, just drag handle for order
    # Optionally, add list_filter if needed
    # list_filter = ('is_active',)

 